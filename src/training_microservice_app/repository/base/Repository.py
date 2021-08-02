from typing import Generic, List, TypeVar

from injector import inject
from sqlalchemy.orm import Query

from repository.base.DatabaseSessionManager import DatabaseSessionManager
from model.entity.BaseEntity import Entity

T = TypeVar('T', bound=Entity)


class Repository(Generic[T]):
    @inject
    def __init__(self, database_session_manager: DatabaseSessionManager):
        self.database_session_manager: DatabaseSessionManager = database_session_manager
        self.type = self.__orig_class__.__args__[0]

    @property
    def table(self):
        return self.database_session_manager.session.query(self.type)

    def insert(self, entity: T):
        self.database_session_manager.session.add(entity)

    def first(self, **kwargs) -> T:
        query: Query = self.table.filter_by(**kwargs)
        return query.first()

    def filter_by(self, **kwargs) -> List[T]:
        query: Query = self.database_session_manager.session.query(self.type)
        return query.filter_by(**kwargs)

    def get(self) -> List[T]:
        query = self.database_session_manager.session.query(self.type)
        return query.all()

    def get_by_id(self, id: str) -> T:
        query = self.database_session_manager.session.query(self.type)
        return query.filter_by(id=id).first()

    def update(self, id: str, update_entity: T):
        entity = self.get_by_id(id)
        self.database_session_manager.session.commit()

    def delete_by_id(self, id: str):
        entity = self.get_by_id(id)
        entity.IsDeleted = 1

    def delete(self, entity: T):
        entity.IsDeleted = 1
