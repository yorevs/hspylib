from abc import ABC
from typing import Optional

from main.hspylib.core.enum.database_type import DatabaseType

from main.hspylib.core.crud.db.mysql.mysql_factory import MySqlFactory
from main.hspylib.core.crud.db.sql_factory import SqlFactory


class SqlFactoryFacade(ABC):
    __factories = {
        DatabaseType.MYSQL.name: MySqlFactory,
        DatabaseType.POSTGRESS_SQL.name: None
    }

    @staticmethod
    def get(db_type: DatabaseType) -> Optional[SqlFactory]:
        return SqlFactoryFacade.__factories[db_type.name.upper()]
