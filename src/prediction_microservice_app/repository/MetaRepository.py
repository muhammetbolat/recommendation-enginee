from typing import Generic, List, TypeVar

from injector import inject
from sqlalchemy.orm import Query

from repository.base.DatabaseSessionManager import DatabaseSessionManager
from model.entity.BaseEntity import Entity

T = TypeVar('T', bound=Entity)


class MetaRepository(Generic[T]):
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

    def get_by_productId(self, productId: str) -> T:
        query = self.database_session_manager.session.query(self.type)
        return query.filter_by(productId=productId).first()

    def save(self, entity: T):
        entity_exist = self.get_by_productId(entity.productId)
        if entity_exist is not None:
            entity_exist.category = entity.category
            entity_exist.subcategory = entity.subcategory
            entity_exist.name = entity.name
        else:
            self.insert(entity)

    def saveAll(self, itemList):
        for item in itemList:
            self.save(item)

    def delete_by_productId(self, productId: str):
        entity = self.get_by_productId(productId)
        self.database_session_manager.session.delete(entity)

    def delete(self, entity: T):
        self.delete_by_productId(entity.productId)

    def commit(self):
        self.database_session_manager.session.commit()
