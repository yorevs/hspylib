from typing import List

from requests.structures import CaseInsensitiveDict as SqlFilter

from main.hspylib.core.crud.db.sql_factory import SqlFactory
from main.hspylib.core.model.entity import Entity


class MySqlFactory(SqlFactory):
    def __init__(self, sql_filename: str):
        super().__init__(sql_filename)
        self.logger.debug('{} created with {} Stubs'.format(self.__class__.__name__, len(self.sql_stubs)))

    def insert(self, entity: Entity) -> str:
        sql = self.sql_stubs['insert']
        columns = str(entity.to_fields()).replace("'", "")
        sql = sql.replace(':columnSet', columns)
        values = str(entity.to_values())
        sql = sql.replace(':valueSet', values)
        return sql

    def select(self, column_set: List[str] = None, filters: SqlFilter = None) -> str:
        sql = self.sql_stubs['select']
        sql = sql.replace(':columnSet', '*') if not column_set else column_set
        sql = sql.replace(':filters', SqlFactory.get_filter_string(filters))
        return sql

    def update(self, entity: Entity, filters: SqlFilter) -> str:
        sql = self.sql_stubs['update']
        sql = sql.replace(':fieldSet', SqlFactory.get_fieldset_string(entity))
        sql = sql.replace(':filters', SqlFactory.get_filter_string(filters))
        return sql

    def delete(self, filters: SqlFilter) -> str:
        sql = self.sql_stubs['delete']
        sql = sql.replace(':filters', SqlFactory.get_filter_string(filters))
        return sql
