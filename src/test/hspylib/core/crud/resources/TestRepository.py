from typing import Tuple
from uuid import UUID

from main.hspylib.core.crud.db.mysql.mysql_repository import MySqlRepository
from main.hspylib.core.model.entity import Entity


class TestEntity(Entity):
    def __init__(self, entity_id: UUID = None, comment: str = None):
        super().__init__(entity_id)
        self.comment = comment

    def __str__(self):
        return 'uuid={} comment={}'.format(self.uuid, self.comment)


class TestRepository(MySqlRepository):
    def __init__(self):
        super().__init__()

    def insert(self, entity: TestEntity):
        super().insert(entity)

    def update(self, entity: TestEntity):
        super().update(entity)

    def delete(self, entity: TestEntity):
        super().delete(entity)

    def row_to_entity(self, row: Tuple) -> TestEntity:
        return TestEntity(row[0], row[1])

    def table_name(self) -> str:
        return 'TEST'
