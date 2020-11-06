from hspylib.core.crud.db.firebase.firebase_repository import FirebaseRepository
from hspylib.core.model.entity import Entity
from test.hspylib.core.crud.resources.TestFirebaseEntity import TestFirebaseEntity


class TestFirebaseRepository(FirebaseRepository):
    def __init__(self):
        super().__init__()

    def insert(self, entity: TestFirebaseEntity):
        super().insert(entity)

    def update(self, entity: TestFirebaseEntity):
        super().update(entity)

    def delete(self, entity: TestFirebaseEntity):
        super().delete(entity)

    def row_to_entity(self, row: dict) -> Entity:
        return TestFirebaseEntity(row['uuid'], row['comment'], row['lucky_number'], row['is_working'])

    def database_name(self) -> str:
        return 'hspylib'
