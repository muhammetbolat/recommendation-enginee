from typing import Generic, List, TypeVar

from injector import inject
from sqlalchemy.orm import Query

from repository.base.DatabaseSessionManager import DatabaseSessionManager
from model.entity.BaseEntity import Entity

T = TypeVar('T', bound=Entity)


class AllDataRepository(Generic[T]):
    @inject
    def __init__(self, database_session_manager: DatabaseSessionManager):
        """
        Constructor method
        """
        self.database_session_manager: DatabaseSessionManager = database_session_manager
        self.type = self.__orig_class__.__args__[0]

    @property
    def table(self):
        return self.database_session_manager.session.query(self.type)

    def first(self, **kwargs) -> T:
        query: Query = self.table.filter_by(**kwargs)
        return query.first()

    def filter_by(self, **kwargs) -> List[T]:
        query: Query = self.database_session_manager.session.query(self.type)
        return query.filter_by(**kwargs)

    def get(self) -> List[T]:
        query = self.database_session_manager.session.query(self.type)
        return query.all()

    def get_by_productId(self, productId: str) -> T:
        query = self.database_session_manager.session.query(self.type)
        return query.filter_by(productId=productId).first()