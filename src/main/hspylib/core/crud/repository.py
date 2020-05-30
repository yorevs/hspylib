from abc import ABC, abstractmethod
from typing import Optional

from core.model.entity import Entity


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
    def find_all(self, filters: str = None) -> Optional[list]:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        pass
