from typing import Tuple

from hspylib.core.crud.db.mysql.mysql_repository import MySqlRepository
from hspylib.core.tools.commons import get_or_default, str_to_bool
from test.hspylib.core.crud.resources.TestEntity import TestEntity


class TestMysqlRepository(MySqlRepository):
    def __init__(self):
        super().__init__()

    def row_to_entity(self, row: Tuple) -> TestEntity:
        return TestEntity(
            get_or_default(row, 0),
            get_or_default(row, 1),
            get_or_default(row, 2),
            str_to_bool(get_or_default(row, 3)))

    def table_name(self) -> str:
        return 'TEST'
