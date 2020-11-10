from hspylib.core.crud.file.file_repository import FileRepository
from test.hspylib.core.crud.resources.TestEntity import TestEntity


class TestFileDbRepository(FileRepository):
    def __init__(self, filename: str):
        super().__init__(filename)

    def dict_to_entity(self, row: dict) -> TestEntity:
        return TestEntity(row['uuid'], row['comment'], row['lucky_number'], row['is_working'])

