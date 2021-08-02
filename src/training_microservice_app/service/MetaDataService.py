from injector import inject

from infrastructor.exception.MetaDataServiceException import MetaDataServiceException
from repository.MetaRepository import MetaRepository
from repository.base.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from model.entity.Meta import Meta
import pandas as pd
import numpy as np
import json


class MetaDataService(IScoped):
    """
    This class is consume data from source and pre-process before inserting/updating databases.
    Final step is to insert/update to DB.
    """
    @inject
    def __init__(self, log: SqlLogger, database_session_manager: DatabaseSessionManager):
        """
        Constructor method
        """
        super().__init__()
        self.log = log
        self.database_session_manager = database_session_manager
        self.meta_repository: MetaRepository[Meta] = MetaRepository[Meta](self.database_session_manager)

    def __read_data(self) -> pd.DataFrame:
        """
        This method reads data from the input stream.
        """
        with open('./data/meta.json') as data_file:
            data = json.load(data_file)

        df_meta = pd.DataFrame = pd.json_normalize(data, 'meta')

        self.log.info("{0} # of meta data is read from the source.".format(len(df_meta)))
        return df_meta

    def __data_pre_processing(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Data pre-processing step. It basically check none, null and not a number values and drop them.
        """
        data = data.drop_duplicates(inplace=False)
        data = data.dropna(how='all', inplace=False)

        # brand field operation
        brandArray = data.brand.unique()
        data["brand"] = data.apply(lambda row: self.__find_none_brand(row, brandArray), axis=1)
        data.fillna({"brand": "anonymous"}, inplace=True)

        self.log.info("{0} # of metadata is pre-processed.".format(len(data)))
        return data

    def __find_none_brand(self, row: pd.DataFrame, brands: np.ndarray) -> str:
        result = None
        brand = row["brand"]
        if row["brand"] is not None:
            result = brand
        else:
            for candidate_brand in brands:
                if candidate_brand is None:
                    continue
                if candidate_brand.lower() in row["name"].lower().split():
                    result = candidate_brand
                    self.log.info("None brand is mapped. brand:{0} , Description:{1}".format(result, row["name"]))

        return result

    def __object_mapper(self, data: pd.DataFrame) -> list:
        """
        This method map data frame object to entity. It will help you to CRUD application to any DBMS.
        """
        listOfMeta = [(Meta(productId=row["productid"],
                            category=row["category"],
                            subcategory=row["subcategory"],
                            name=row["name"],
                            brand=row["brand"]
                            )) for _, row in data.iterrows()]

        self.log.info("{0} # of metadata is mapped to meta object.".format(len(listOfMeta)))

        return listOfMeta

    def save_data(self) -> None:
        """
        This methods save data to database management system.
        """
        try:
            data = self.__read_data()
            data = self.__data_pre_processing(data)
            metas = self.__object_mapper(data)

            self.meta_repository.saveAll(metas)
            self.meta_repository.commit()

            self.log.info("{0} # of product are saved/updated in DB.".format(len(metas)))

        except Exception as ex:
            err: str = "Error is occured, err: {}".format(ex)
            self.log.error(ex)
            raise MetaDataServiceException(err)
