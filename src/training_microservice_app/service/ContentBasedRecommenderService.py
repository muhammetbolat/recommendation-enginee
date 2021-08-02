import json
from typing import List

from injector import inject

from infrastructor.exception.ContentBasedRecommenderServiceException import ContentBasedRecommenderServiceException
from model.entity.AllData import AllData
from model.entity.CartScore import CartScore
from model.entity.ContentScore import ContentScore
from model.entity.PassedDayScore import PassedDayScore
from repository.AllDataRepository import AllDataRepository
from repository.CartScoreRepository import CartScoreRepository
from repository.ContentScoreRepository import ContentScoreRepository
from repository.PassedDayScoreRepository import PassedDayScoreRepository
from repository.base.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from snowballstemmer import TurkishStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommenderService(IScoped):
    """
    Constructor method
    """
    @inject
    def __init__(self, log: SqlLogger, database_session_manager: DatabaseSessionManager):
        super().__init__()
        self.log = log
        self.database_session_manager = database_session_manager
        self.passed_day_score_repository: PassedDayScoreRepository[PassedDayScore] = \
            PassedDayScoreRepository[PassedDayScore](self.database_session_manager)
        self.all_data_repository: AllDataRepository[AllData] = AllDataRepository[AllData](self.database_session_manager)
        self.content_score_repository: ContentScoreRepository[ContentScore] = \
            ContentScoreRepository[ContentScore](self.database_session_manager)
        # Turkish stopwords
        self.stops = set(stopwords.words('turkish'))
        # Turkish letters regex pattern. Non-Turkish letter characters such as punctuations and numbers
        self.exc_letters_pattern = '[^a-zçğışöü]'
        # Turkish stemmer
        self.turkStem = TurkishStemmer()
        self.unit_pattern: str = '(?P<a>\d+\.\d+|\d+)\s*(?P<b>[a-z%]+)'
        self.turkish_quantity_pattern = "([0-9])\'([a-z]+)"
        self.special_letters: dict = {'î': 'i', 'â': 'a'}
        self.indices = None
        self.cosine_sim = None
        self.products = None

    def __get_data(self) -> pd.DataFrame:
        """

        """
        allData: List[AllData] = self.all_data_repository.get()
        df_all: pd.DataFrame = self.__object_demapper(allData)
        return df_all

    def __object_demapper(self, data: list) -> pd.DataFrame:
        """
        This method de-mapp entity objects to data frame. It will help programmer to analys using pandas library.
        """
        data = pd.DataFrame.from_records([s.to_dict() for s in data])

        self.log.info("{0} # of all data is de-mapped to object.".format(len(data)))

        return data

    def __text_pre_processing(self, text: str, brand_array: np.ndarray) -> str:
        # 1. convert to lowercase
        text = text.lower()

        # 2. remove measure of units remove as 100 gr, 1 kg, 50m
        text = re.sub(self.unit_pattern, '', text)

        # 3. remove as 5'li, 10'lu
        text = re.sub(self.turkish_quantity_pattern, '', text)

        # 4. replace special letter
        for sp_let, tr_let in self.special_letters.items():
            text = re.sub(sp_let, tr_let, text)

        # 5. remove non-turkish letters
        text = re.sub(self.exc_letters_pattern, ' ', text)

        # 6. remove stopwords and stem
        wordList = text.split()

        wordList = [self.turkStem.stemWord(w) for w in wordList
                    if (w not in self.stops and len(w) > 2 and w not in brand_array)]

        return ' '.join(wordList)

    def __mixture(self, df_all: pd.DataFrame) -> pd.Series:
        """

        """
        return (df_all.brand + " " + df_all.category + " " + df_all.subcategory + " " + df_all.name_processed).str.lower()

    def __count_vectorizer(self, df: pd.DataFrame):
        count = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0)
        count_matrix = count.fit_transform(df.mixture)
        self.log.info("CountVectorizing is calculated.")
        return count_matrix

    def predict(self, productid):
        idx = self.indices.loc[productid]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        product_indices = [i[0] for i in sim_scores]
        cos_scores = [i[1] for i in sim_scores]
        productslist = self.products.iloc[product_indices]
        dict_result = {"productid": list(productslist.values), "score": cos_scores}

        return json.dumps(dict_result)


    def __object_mapper(self, data: pd.DataFrame) -> list:
        """
        This method map data frame object to entity. It will help you to CRUD application to any DBMS.
        """
        listOfAllData = [(ContentScore(productId=row.productId, score=row.content_score,))
                         for _, row in data.iterrows()]

        self.log.info("{0} # of content score data is mapped to object.".format(len(listOfAllData)))

        return listOfAllData

    def __save_to_db(self, scores: list) -> None:
        """
        Save results to database management system.
        """

        self.content_score_repository.saveAll(scores)
        self.content_score_repository.commit()

        self.log.info("{0} # of content scores are saved/updated in DB.".format(len(scores)))

    def getScores(self, products: list) -> List[ContentScore]:
        """
        This method gets score which are calculated.
        """
        productList: List[ContentScore] = self.content_score_repository.get_by_products(products)
        self.log.info("content score is fetched.")
        return productList

    def fit(self):
        """
        Fit/train content based recommender system to call other private methods.
        """
        try:
            df: pd.DataFrame = self.__get_data()

            brand_array: np.ndarray = df.brand.str.lower().unique()

            df["name_processed"] = df.name.apply(lambda x: self.__text_pre_processing(x, brand_array))
            self.log.info("Text-preprocessing is finished.")

            df["mixture"] = self.__mixture(df)

            count_matrix = self.__count_vectorizer(df)

            self.cosine_sim = cosine_similarity(count_matrix, count_matrix)
            self.log.info("Cosine similarity is calculated.")

            df = df.reset_index()
            self.products = df.productId
            self.indices = pd.Series(df.index, index=df['productId'])
            df["content_score"] = df.productId.apply(lambda x: self.predict(x))
            self.log.info("Content scores are calculated.")

            contentScores: list = self.__object_mapper(df)

            self.__save_to_db(contentScores)

            self.indices = None
            self.cosine_sim = None
            self.products = None

            self.log.info("Content based recommender training is finished.")

        except Exception as ex:
            err: str = "Error is occured, err: {}".format(ex)
            self.log.error(ex)
            raise ContentBasedRecommenderServiceException(err)















