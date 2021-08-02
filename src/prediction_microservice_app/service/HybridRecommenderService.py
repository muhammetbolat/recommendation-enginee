from injector import inject

from infrastructor.exception.HybridRecommenderServiceException import HybridRecommenderServiceException
from model.entity.CartScore import CartScore
from model.entity.ContentScore import ContentScore
from model.entity.PassedDayScore import PassedDayScore
from repository.CartScoreRepository import CartScoreRepository
from repository.ContentScoreRepository import ContentScoreRepository
from repository.PassedDayScoreRepository import PassedDayScoreRepository
from repository.base.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
import pandas as pd
import json


class HybridRecommenderService(IScoped):
    """
    Constructor method
    """
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 log: SqlLogger,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_session_manager = database_session_manager
        self.content_score_repository: ContentScoreRepository[ContentScore] = \
            ContentScoreRepository[ContentScore](self.database_session_manager)
        self.cart_score_repository: CartScoreRepository[CartScore] = \
            CartScoreRepository[CartScore](self.database_session_manager)
        self.passed_day_score_repository: PassedDayScoreRepository[PassedDayScore] = \
            PassedDayScoreRepository[PassedDayScore](self.database_session_manager)
        self.log = log

    def __fillScores(self, contentScores):
        """
        This method is to find scores which are stored in dB.
        """

        list_of_data_frames = list()

        for cntScr in contentScores:
            res = json.loads(cntScr.score)

            df_pro = pd.DataFrame(res)
            df_pro["productId_requested"] = cntScr.productId
            df_pro["cart_score"] = self.cart_score_repository.get_by_products(list(df_pro.productid))
            df_pro["passed_day_score"] =self.passed_day_score_repository.get_by_products(list(df_pro.productid))
            df_pro["final_score"] = (df_pro.score + df_pro.cart_score + df_pro.passed_day_score) / 3
            best_product = df_pro.set_index("productid")["final_score"].idxmax(axis="columns")
            df_pro["bias_score"] = df_pro.apply(lambda x: self.__set_bias_score(x, best_product), axis=1)
            list_of_data_frames.append(df_pro)
        df = pd.concat(list_of_data_frames)
        return df

    def __set_bias_score(self, row, best_score):
        """
        the method is to calculate the first products.
        """
        if row.productid == best_score:
            result = 1
        else:
            result = row.final_score

        return result

    def __get_top(self, result, top=10):
        """
        get the top products.
        """
        result = result.sort_values(by="bias_score", ascending=False).drop_duplicates(subset='productid', keep="first")[:top].productid

        return list(result)

    def predict(self, products: list):
        """
        This is prediction method.
        """
        try:
            self.log.info("Prediction is started.")

            contentScores: list = self.content_score_repository.get_by_products(products)

            df = self.__fillScores(contentScores)

            result = self.__get_top(df)
            self.log.info("Top values are calculated.")

            self.log.info("Prediction is finished.")

            return result

        except Exception as ex:
            msg: str = "Undefined error is occured in Hybrid recommender service. "
            self.log.error(msg + "err: {}".format(ex))
            raise HybridRecommenderServiceException(msg)






