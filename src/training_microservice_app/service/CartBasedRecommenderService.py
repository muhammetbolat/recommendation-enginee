from typing import List

from injector import inject

from infrastructor.exception.CartBasedRecommenderServiceException import CartBasedRecommenderServiceException
from model.entity.AllData import AllData
from model.entity.CartScore import CartScore
from repository.AllDataRepository import AllDataRepository
from repository.CartScoreRepository import CartScoreRepository
from repository.base.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
import pandas as pd


class CartBasedRecommenderService(IScoped):
    """
    Cart based recommender training service
    """

    @inject
    def __init__(self, log: SqlLogger, database_session_manager: DatabaseSessionManager):
        """
        Constructor method
        """
        super().__init__()
        self.log = log
        self.database_session_manager = database_session_manager
        self.cart_score_repository: CartScoreRepository[CartScore] = \
            CartScoreRepository[CartScore](self.database_session_manager)
        self.all_data_repository: AllDataRepository[AllData] = AllDataRepository[AllData](self.database_session_manager)
        self.m_df = None

    def __object_demapper(self, data: list) -> pd.DataFrame:
        """
        This method de-mapp entity objects to data frame. It will help programmer to analys using pandas library.
        """
        data = pd.DataFrame.from_records([s.to_dict() for s in data])

        self.log.info("{0} # of all data is de-mapped to object.".format(len(data)))

        return data

    def __object_mapper(self, data: pd.DataFrame) -> list:
        """
        This method map data frame object to entity. It will help you to CRUD application to any DBMS.
        """
        listOfAllData = [(CartScore(productId=row.productId, score=row.cartScore, )) for _, row in data.iterrows()]

        self.log.info("{0} # of cart score data is mapped to object.".format(len(listOfAllData)))

        return listOfAllData

    def __calculate_m_value(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        This method calculates m value order by sub-category. Each categories' product will be score to each other.
        """
        m_subcat_df = data[["subcategory", "numberOfCart"]].groupby(by=["subcategory"]).quantile(0.9)
        self.log.info("cart m values are calculated.")
        return m_subcat_df

    def __cart_weighted_rating(self, row: pd.DataFrame) -> float:
        """
        This method calculate weighted value for all products.
        """
        v = row['numberOfCart']
        subCategory = row['subcategory']
        m_cat = self.m_df.loc[subCategory]["numberOfCart"]
        return v / (v + m_cat)

    def __transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform and calculate score according to sub-category.
        """
        data["cartScore"] = data.apply(self.__cart_weighted_rating, axis=1)
        self.log.info("cart scores are calculated.")
        return data[["productId", "cartScore"]]

    def __save_to_db(self, scores: list) -> None:
        """
        Save results to database management system.
        """
        self.cart_score_repository.saveAll(scores)
        self.cart_score_repository.commit()

        self.log.info("{0} # of cart scores are saved/updated in DB.".format(len(scores)))

    def getScores(self, products: list) -> list:
        """
        This method gets score which are calculated.
        """
        productScores: list = self.cart_score_repository.get_by_products(products)
        return productScores

    def fit(self) -> None:
        """
        Fit/train cart based recommender system to call other private methods.
        """
        try:
            allData: List[AllData] = self.all_data_repository.get()
            df_all: pd.DataFrame = self.__object_demapper(allData)
            self.m_df: pd.DataFrame = self.__calculate_m_value(df_all)
            df_all: pd.DataFrame = self.__transform(df_all)

            cartScores: list = self.__object_mapper(df_all)

            self.__save_to_db(cartScores)

            self.log.info("Cart based recommender training is finished.")

        except Exception as ex:
            err: str = "Error is occured, err: {}".format(ex)
            self.log.error(ex)
            raise CartBasedRecommenderServiceException(err)
