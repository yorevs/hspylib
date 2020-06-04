from typing import List, Optional

from requests.structures import CaseInsensitiveDict as SqlFilter

from main.hspylib.core.crud.db.sql_factory import SqlFactory
from main.hspylib.core.model.entity import Entity


class MySqlFactory(SqlFactory):
    def __init__(self, sql_filename: str):
        super().__init__(sql_filename)
        self.logger.debug('{} created with {} Stubs'.format(self.__class__.__name__, len(self.sql_stubs)))

    def insert(self, entity: Entity) -> Optional[str]:
        sql = self.sql_stubs['insert']\
            .replace(':columnSet', str(entity.to_fields()).replace("'", ""))\
            .replace(':valueSet', str(entity.to_values()))
        return sql

    def select(self, column_set: List[str] = None, filters: SqlFilter = None) -> Optional[str]:
        sql = self.sql_stubs['select']\
            .replace(':columnSet', '*' if not column_set else ', '.join(column_set))\
            .replace(':filters', SqlFactory.get_filter_string(filters))
        return sql

    def update(self, entity: Entity, filters: SqlFilter) -> Optional[str]:
        sql = self.sql_stubs['update']\
            .replace(':fieldSet', SqlFactory.get_fieldset_string(entity))\
            .replace(':filters', SqlFactory.get_filter_string(filters))
        return sql

    def delete(self, filters: SqlFilter) -> Optional[str]:
        sql = self.sql_stubs['delete']\
            .replace(':filters', SqlFactory.get_filter_string(filters))
        return sql
