from requests.structures import CaseInsensitiveDict

from main.hspylib.core.crud.db.sql_factory import SqlFactory
from main.hspylib.core.model.entity import Entity


class MySqlFactory(SqlFactory):
    def __init__(self, sql_filename: str):
        super().__init__(sql_filename)
        self.logger.debug('{} created with {} Stubs'.format(self.__class__.__name__, len(self.sql_stubs)))

    def insert(self, entity: Entity) -> str:
        sql = self.sql_stubs['insert']
        sql = sql.replace(':tableName', entity.get_table_name())
        columns = str(self.column_set(entity)).replace("'", "")
        sql = sql.replace(':columnSet', columns)
        values = str(self.values_set(entity))
        sql = sql.replace(':valueSet', values)
        return sql

    def select(self, filters: CaseInsensitiveDict) -> str:
        sql = self.sql_stubs['select']
        return sql

    def update(self, entity: Entity, filters: CaseInsensitiveDict) -> str:
        sql = self.sql_stubs['update']
        return sql

    def delete(self, filters: CaseInsensitiveDict) -> str:
        sql = self.sql_stubs['delete']
        return sql
