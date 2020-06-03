from abc import ABC, abstractmethod

from requests.structures import CaseInsensitiveDict

from main.hspylib.core.meta.singleton import Singleton
from main.hspylib.core.model.entity import Entity


class SqlFactory(metaclass=Singleton):
    @staticmethod
    def read_stubs(self, filename: str, tablename: str):
        pass

    @abstractmethod
    def insert(self, entity: Entity):
        pass

    @abstractmethod
    def select(self, filters: CaseInsensitiveDict):
        pass

    @abstractmethod
    def update(self, entity: Entity, filters: CaseInsensitiveDict):
        pass

    @abstractmethod
    def delete(self, filters: CaseInsensitiveDict):
        pass
