from abc import abstractmethod

from requests.structures import CaseInsensitiveDict

from main.hspylib.core.crud.db.sql_factory import SqlFactory
from main.hspylib.core.meta.singleton import Singleton
from main.hspylib.core.model.entity import Entity


class MySqlFactory(metaclass=Singleton, SqlFactory):
    INSTANCE = None

    def __init__(self):
        self.__sql_stubs = None

    @abstractmethod
    def insert(self, entity: Entity):
        pass

    @abstractmethod
    def select(self, filters: CaseInsensitiveDict[str, str]):
        pass

    @abstractmethod
    def update(self, entity: Entity, filters: CaseInsensitiveDict[str, str]):
        pass

    @abstractmethod
    def delete(self, filters: CaseInsensitiveDict[str, str]):
        pass

