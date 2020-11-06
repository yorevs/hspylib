from abc import ABC, abstractmethod
from typing import Optional

from hspylib.core.model.entity import Entity
from requests.structures import CaseInsensitiveDict


class Repository(ABC):
    @abstractmethod
    def insert(self, entity: Entity):
        pass

    @abstractmethod
    def update(self, entity: Entity):
        pass

    @abstractmethod
    def delete(self, entity: Entity):
        pass

    @abstractmethod
    def find_all(self, filters: CaseInsensitiveDict = None) -> Optional[list]:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        pass
