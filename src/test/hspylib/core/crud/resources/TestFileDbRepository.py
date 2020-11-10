import uuid
from typing import Optional

from test.hspylib.core.crud.resources.TestFileDbEntity import TestFileDbEntity

from hspylib.core.crud.file.file_repository import FileRepository


class TestFileDbRepository(FileRepository):
    def __init__(self, filename: str):
        super().__init__(filename)

    def insert(self, entity: TestFileDbEntity):
        super().insert(entity)

    def update(self, entity: TestFileDbEntity):
        super().update(entity)

    def delete(self, entity: TestFileDbEntity):
        super().delete(entity)

    def dict_to_entity(self, row: dict) -> TestFileDbEntity:
        return TestFileDbEntity(row['uuid'], row['comment'], row['lucky_number'], row['is_working'])

