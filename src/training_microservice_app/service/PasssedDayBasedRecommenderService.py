from typing import List

from injector import inject

from infrastructor.exception.PassedDayBasedRecommenderServiceException import PassedDayBasedRecommenderServiceException
from model.entity.AllData import AllData
from model.entity.CartScore import CartScore
from model.entity.PassedDayScore import PassedDayScore
from repository.AllDataRepository import AllDataRepository
from repository.CartScoreRepository import CartScoreRepository
from repository.PassedDayScoreRepository import PassedDayScoreRepository
from repository.base.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
import pandas as pd


class PassedDayBasedRecommenderService(IScoped):
    """
    Passed day based recommender training service
    """
    @inject
    def __init__(self, log: SqlLogger, database_session_manager: DatabaseSessionManager):
        """
        Constructor method
        """
        super().__init__()
        self.log = log
        self.database_session_manager = database_session_manager
        self.passed_day_score_repository: PassedDayScoreRepository[PassedDayScore] = \
            PassedDayScoreRepository[PassedDayScore](self.database_session_manager)
        self.all_data_repository: AllDataRepository[AllData] = AllDataRepository[AllData](self.database_session_manager)
        self.m_subcat_passedday_df = None

    def __object_demapper(self, data: list) -> pd.DataFrame:
        """
        This method de-map entity objects to data frame. It will help programmer to analys using pandas library.
        """
        data = pd.DataFrame.from_records([s.to_dict() for s in data])

        self.log.info("{0} # of passedday score data is mapped to object.".format(len(data)))

        return data

    def __object_mapper(self, data: pd.DataFrame) -> list:
        """
        This method map data frame object to entity. It will help you to CRUD application to any DBMS.
        """
        listOfAllData = [(PassedDayScore(productId=row.productId, score=row.passedDayScore,))
                         for _, row in data.iterrows()]

        self.log.info("{0} # of passedday score data is mapped to object.".format(len(listOfAllData)))

        return listOfAllData

    def __calculate_m_value(self, data: pd.DataFrame) -> None:
        """
        This method calculates m value order by sub-category. Each categories' product will be score to each other.
        """
        self.m_subcat_passedday_df = data[["subcategory", "passedDay"]].groupby(by=["subcategory"]).quantile(0.9)
        self.log.info("passed day m values are calculated.")

    def __passed_day_weighted_rating(self, raw: pd.DataFrame) -> float:
        """
        This method calculate weighted value for all products.
        """
        v = raw['passedDay']
        subCategory = raw['subcategory']
        m_cat = self.m_subcat_passedday_df.loc[subCategory]['passedDay']
        return 1 - v / (v + m_cat)

    def __transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform and calculate score according to sub-category.
        """
        data["passedDayScore"] = data.apply(self.__passed_day_weighted_rating, axis=1)
        self.log.info("passedday scores are calculated.")
        return data[["productId", "passedDayScore"]]

    def getScores(self, products: list) -> list:
        """
        This method gets score which are calculated.
        """
        productScores: list = self.passed_day_score_repository.get_by_products(products)
        return productScores

    def __save_to_db(self, scores: list) -> None:
        """
        Save results to database management system.
        """

        self.passed_day_score_repository.saveAll(scores)
        self.passed_day_score_repository.commit()

        self.log.info("{0} # of passed day scores are saved/updated in DB.".format(len(scores)))

    def fit(self) -> None:
        """
        Fit/train passed day based recommender system to call other private methods.
        """
        try:
            allData: List[PassedDayScore] = self.all_data_repository.get()
            df_all: pd.DataFrame = self.__object_demapper(allData)
            self.__calculate_m_value(df_all)
            df_all: pd.DataFrame = self.__transform(df_all)

            passedDayScores: list = self.__object_mapper(df_all)

            self.__save_to_db(passedDayScores)

            self.log.info("Passed day based recommender training is finished.")

        except Exception as ex:
            err: str = "Error is occured, err: {}".format(ex)
            self.log.error(ex)
            raise PassedDayBasedRecommenderServiceException(err)
