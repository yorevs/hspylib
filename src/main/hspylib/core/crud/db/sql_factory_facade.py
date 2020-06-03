from abc import ABC
from typing import Optional

from main.hspylib.core.crud.db.mysql.mysql_factory import MySqlFactory
from main.hspylib.core.crud.db.sql_factory import SqlFactory
from main.hspylib.core.enum.database_type import DatabaseType


class SqlFactoryFacade(ABC):
    _cache = {}
    _factories = {
        DatabaseType.MYSQL.name: MySqlFactory,
        DatabaseType.POSTGRESS_SQL.name: None
    }

    @staticmethod
    def __create_or_get(db_type: DatabaseType, sql_filename: str) -> SqlFactory:
        factory = SqlFactoryFacade._cache[sql_filename] if sql_filename in SqlFactoryFacade._cache else None
        if not factory:
            factory = SqlFactoryFacade._factories[db_type.name.upper()](sql_filename)
            SqlFactoryFacade._cache[sql_filename] = factory

        return factory

    @staticmethod
    def get(db_type: DatabaseType, sql_filename: str) -> Optional[SqlFactory]:
        return SqlFactoryFacade.__create_or_get(db_type, sql_filename)
