from injector import inject

from infrastructor.exception.EventDataServiceException import EventDataServiceException
from repository.EventRepository import EventRepository
from repository.base.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from model.entity.Event import Event
import pandas as pd
import json


class EventDataService(IScoped):
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
        self.event_repository: EventRepository[Event] = EventRepository[Event](self.database_session_manager)

    def __read_data(self) -> pd.DataFrame:
        """
        This method reads data from the input stream.
        """
        with open('./data/events.json') as data_file:
            data = json.load(data_file)

        df_events: pd.DataFrame = pd.json_normalize(data, 'events')

        df_events.drop(["event", "sessionid"], axis=1, inplace=True)

        self.log.info("{0} # of event is read from the source.".format(len(df_events)))
        return df_events

    def __data_pre_processing(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Data pre-processing step. It basically check none, null and not a number values and drop them.
        Change dtype of price and eventtime fields.
        """
        self.log.info("EVENT Data pre-processing is handling..")
        data = data.drop_duplicates(inplace=False)
        data = data.dropna(inplace=False)
        data["price"] = data.price.astype(float)
        data["eventtime"] = pd.to_datetime(data.eventtime)

        self.log.info("{0} # of event is pre-processed.".format(len(data)))
        return data

    def __data_group_by_operation(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Groupby operation to calculate sum of cart by product. It helps to calculation and reduce transaction to DB.
        """

        number_of_cart = data.groupby(by="productid").count().rename(columns={'eventtime': 'numberOfCart'})

        last_date = data[["productid", "eventtime"]].groupby(by="productid").max()

        data = number_of_cart.merge(last_date, on="productid").reset_index()[["productid", "numberOfCart", "eventtime"]]

        return data

    def __day_calculation(self, data: pd.DataFrame, now='2020-08-01T12Z') -> pd.DataFrame:
        """
        This method take the difference between days. The newest record in dataframe is 2020-08-01.
        So now variable's default value is set to that date. For the streaming processing,
        it should replace with datetime.now()
        """
        data["day"] = (pd.Timestamp(now) - data.eventtime.apply(pd.to_datetime)).apply(lambda x: x.days)
        data.drop(["eventtime"], axis=1, inplace=True)
        return data

    def __object_mapper(self, data: pd.DataFrame) -> list:
        """
        This method map data frame object to entity. It will help you to CRUD application to any DBMS.
        """
        listOfEvent = [(Event(productId=row.productid,
                              numberOfCart=row.numberOfCart,
                              price=row.price,
                              passedDay=row.day
                              )) for _, row in data.iterrows()]

        self.log.info("{0} # of product is mapped to object.".format(len(listOfEvent)))

        return listOfEvent

    def save_data(self):
        """
        This methods save data to database management system.
        """
        try:
            data = self.__read_data()
            data = self.__data_pre_processing(data)
            data_grouped = self.__data_group_by_operation(data)

            data = data_grouped.merge(data, on=["productid", "eventtime"])

            data = self.__day_calculation(data)

            events = self.__object_mapper(data)

            for event in events:
                db_event = self.event_repository.first(productId=event.productId)
                if db_event is not None:
                    event.numberOfCart += db_event.numberOfCart
                    # If product_id exist in DB, we should check the last cart date and decide streaming record
                    # s new or not. If it is new, we should replace new price and count number of cart.
                    # The new price makes sense for customer to think the latest price of the order.
                    if db_event.passedDay < event.passedDay:
                        event.price = db_event.price
                        event.passedDay = db_event.passedDay

                self.event_repository.save(event)

            self.event_repository.commit()

            self.log.info("{0} # of product are saved/updated in DB.".format(len(events)))

        except Exception as ex:
            err: str = "Error is occured, err: {}".format(ex)
            self.log.error(ex)
            raise EventDataServiceException(err)
