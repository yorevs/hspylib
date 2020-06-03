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

    def select(self, filters: SqlFilter) -> str:
        sql = self.sql_stubs['select'].replace(':columnSet', '*')
        filter_set = ''
        for key, value in filters.items():
            filter_set += "AND {} = '{}'".format(key, value)
        sql = sql.replace(':filters', filter_set)
        return sql

    def update(self, entity: Entity, filters: SqlFilter) -> str:
        sql = self.sql_stubs['update']
        fields = entity.fieldset()
        field_set = ''
        for key, value in fields.items():
            field_set += "{}{} = '{}'".format(', ' if field_set else '', key, value)
        sql = sql.replace(':fieldSet', field_set)
        filter_set = ''
        for key, value in filters.items():
            filter_set += "AND {} = '{}'".format(key, value)
        sql = sql.replace(':filters', filter_set)
        return sql

    def delete(self, filters: SqlFilter) -> str:
        sql = self.sql_stubs['delete']
        return sql
