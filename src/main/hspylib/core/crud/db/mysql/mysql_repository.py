import os
import sys
import uuid
from abc import abstractmethod
from typing import Optional, Tuple

import pymysql
from pymysql.err import OperationalError, ProgrammingError
from requests.structures import CaseInsensitiveDict as SqlFilter

from main.hspylib.core.crud.db.db_repository import DBRepository
from main.hspylib.core.crud.db.sql_factory_facade import SqlFactoryFacade
from main.hspylib.core.enum.database_type import DatabaseType
from main.hspylib.core.model.entity import Entity


class MySqlRepository(DBRepository):
    __connections = {}

    def __init__(self):
        super().__init__()
        self._connector = None
        self._cursor = None
        self._sql_factory = SqlFactoryFacade.get(
            DatabaseType.MYSQL, '{}/sql/mysql_stubs.sql'.format(os.path.dirname(__file__)))

    def __str__(self):
        return "{}@{}:{}/{}".format(self.user, self.hostname, self.port, self.database)

    def is_connected(self):
        return self._connector is not None

    def connect(self):
        if not self.is_connected():
            cache_key = self.__str__()
            if cache_key in MySqlRepository.__connections:
                self._connector = MySqlRepository.__connections[cache_key]
                self._cursor = self._connector.cursor()
                assert self.is_connected(), "Not connected to the database"
            else:
                try:
                    self._connector = pymysql.connect(
                        host=self.hostname,
                        user=self.user,
                        port=self.port,
                        password=self.password,
                        database=self.database
                    )
                    assert self.is_connected(), "Unable to connect to the database"
                    self._cursor = self._connector.cursor()
                    self.logger.debug('Connection to {} established'.format(str(self)))
                    MySqlRepository.__connections[cache_key] = self._connector
                except OperationalError:
                    self.logger.error('Unable to connect to {}'.format(str(self)))
                    sys.exit(1)

    def disconnect(self):
        if self.is_connected():
            cache_key = self.__str__()
            self._connector.close()
            self._connector = None
            del MySqlRepository.__connections[cache_key]
            self.logger.debug('Disconnected from {}.'.format(str(self)))
        else:
            self.logger.error('Unable to disconnect from {}'.format(str(self)))
            sys.exit(1)

        return self._connector

    def insert(self, entity: Entity):
        if self.is_connected():
            entity.uuid = entity.uuid if entity.uuid is not None else str(uuid.uuid4())
            stm = self._sql_factory.insert(entity)
            stm = stm.replace(':tableName', self.table_name())
            self.logger.debug('Executing SQL statement: {}'.format(stm))
            self._cursor.execute(stm)
            self._connector.commit()
        else:
            self.logger.error('Not connected to database.')

    def update(self, entity: Entity):
        if self.is_connected():
            stm = self._sql_factory.update(entity, filters=SqlFilter({"UUID": '{}'.format(entity.uuid)}))
            stm = stm.replace(':tableName', self.table_name())
            self.logger.debug('Executing SQL statement: {}'.format(stm))
            self._cursor.execute(stm)
        else:
            self.logger.error('Not connected to database.')

    def delete(self, entity: Entity):
        if self.is_connected():
            stm = self._sql_factory.delete(filters=SqlFilter({"UUID": '{}'.format(entity.uuid)}))
            stm = stm.replace(':tableName', self.table_name())
            self.logger.debug('Executing SQL statement: {}'.format(stm))
            self._cursor.execute(stm)
            self._connector.commit()

    def find_all(self, sql_filters: SqlFilter = None) -> Optional[list]:
        if self.is_connected():
            stm = self._sql_factory.select(filters=sql_filters)
            stm = stm.replace(':tableName', self.table_name())
            self.logger.debug('Executing SQL statement: {}'.format(stm))
            try:
                self._cursor.execute(stm)
                result = self._cursor.fetchall()
                ret_val = []
                for next_row in result:
                    ret_val.append(self.row_to_entity(next_row))
                return ret_val
            except ProgrammingError:
                return None
        else:
            self.logger.error('Not connected to database.')

    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        if self.is_connected():
            if entity_id:
                stm = self._sql_factory.select(filters=SqlFilter({"UUID": '{}'.format(entity_id)}))
                stm = stm.replace(':tableName', self.table_name())
                self.logger.debug('Executing SQL statement: {}'.format(stm))
                self._cursor.execute(stm)
                result = self._cursor.fetchall()
                return self.row_to_entity(result[0]) if len(result) > 0 else None
            else:
                return None
        else:
            self.logger.error('Not connected to database.')

    def execute(self, sql_statement: str):
        if self.is_connected():
            self._cursor.execute(sql_statement)
            self.logger.debug('Executing SQL statement: {}'.format(sql_statement))
        else:
            self.logger.error('Not connected to database.')

    @abstractmethod
    def row_to_entity(self, row: Tuple) -> Entity:
        pass

    @abstractmethod
    def table_name(self) -> str:
        pass
