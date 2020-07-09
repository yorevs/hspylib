from typing import Optional

from requests.structures import CaseInsensitiveDict

from main.hspylib.core.crud.db.firebase.firebase_config import FirebaseConfig
from main.hspylib.core.crud.repository import Repository
from main.hspylib.core.model.entity import Entity


class FirebaseRepository(Repository):
    def __init__(self):
        self.payload = None
        self.config = FirebaseConfig()

    def __str__(self):
        return str(self.payload)

    def insert(self, entity: Entity):
        pass

    def update(self, entity: Entity):
        pass

    def delete(self, entity: Entity):
        pass

    def find_all(self, filters: CaseInsensitiveDict = None) -> Optional[list]:
        pass

    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        pass
