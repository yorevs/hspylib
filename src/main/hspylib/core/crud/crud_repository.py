from abc import ABC, abstractmethod
from typing import Optional, List

from requests.structures import CaseInsensitiveDict

from hspylib.core.model.entity import Entity


class CrudRepository(ABC):
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
    def find_all(self, filters: CaseInsensitiveDict = None) -> List[Entity]:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        pass
