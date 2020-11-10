from hspylib.core.crud.db.firebase.firebase_repository import FirebaseRepository
from hspylib.core.model.entity import Entity
from test.hspylib.core.crud.resources.TestEntity import TestEntity


class TestFirebaseRepository(FirebaseRepository):
    def __init__(self):
        super().__init__()

    def row_to_entity(self, row: dict) -> Entity:
        return TestEntity(row['uuid'], row['comment'], row['lucky_number'], row['is_working'])

    def database_name(self) -> str:
        return 'hspylib'
