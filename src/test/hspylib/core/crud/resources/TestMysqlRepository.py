from typing import Tuple

from hspylib.core.crud.db.mysql.mysql_repository import MySqlRepository
from test.hspylib.core.crud.resources.TestMysqlEntity import TestMysqlEntity


class TestMysqlRepository(MySqlRepository):
    def __init__(self):
        super().__init__()

    def insert(self, entity: TestMysqlEntity):
        super().insert(entity)

    def update(self, entity: TestMysqlEntity):
        super().update(entity)

    def delete(self, entity: TestMysqlEntity):
        super().delete(entity)

    def row_to_entity(self, row: Tuple) -> TestMysqlEntity:
        return TestMysqlEntity(row[0], row[1] if len(row) > 1 else None)

    def table_name(self) -> str:
        return 'TEST'
