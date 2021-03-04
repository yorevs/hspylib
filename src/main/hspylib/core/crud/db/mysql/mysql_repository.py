import sys
import uuid
from abc import abstractmethod
from typing import Optional, Tuple, List

import pymysql
from pymysql.err import OperationalError, ProgrammingError
from requests.structures import CaseInsensitiveDict as SqlFilter

from hspylib.core.crud.db.db_repository import DBRepository
from hspylib.core.crud.db.sql_factory import SqlFactory
from hspylib.core.model.entity import Entity


class MySqlRepository(DBRepository):
    _connections = {}

    def __init__(self):
        super().__init__()
        self._connector = None
        self._cursor = None
        self._sql_factory = SqlFactory()

    def is_connected(self):
        return self._connector is not None

    def connect(self):
        if not self.is_connected():
            cache_key = self.__str__()
            if cache_key in MySqlRepository._connections:
                self._connector = MySqlRepository._connections[cache_key]
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
                    MySqlRepository._connections[cache_key] = self._connector
                except (OperationalError, ConnectionRefusedError):
                    self.logger.error('Unable to connect to {}'.format(str(self)))
                    sys.exit(1)

    def disconnect(self):
        if self.is_connected():
            cache_key = self.__str__()
            self._connector.close()
            self._connector = None
            del MySqlRepository._connections[cache_key]
            self.logger.debug('Disconnected from {}.'.format(str(self)))
        else:
            self.logger.error('Unable to disconnect from {}'.format(str(self)))
            sys.exit(1)

        return self._connector

    def insert(self, entity: Entity):
        if self.is_connected():
            entity.uuid = entity.uuid if entity.uuid is not None else str(uuid.uuid4())
            stm = self._sql_factory\
                .insert(entity)\
                .replace(':tableName', self.table_name())
            self.logger.debug('Executing SQL statement: {}'.format(stm))
            self._cursor.execute(stm)
        else:
            self.logger.error('Not connected to database.')

    def update(self, entity: Entity):
        if self.is_connected():
            stm = self._sql_factory\
                .update(entity, filters=SqlFilter({"UUID": '{}'.format(entity.uuid)}))\
                .replace(':tableName', self.table_name())
            self.logger.debug('Executing SQL statement: {}'.format(stm))
            self._cursor.execute(stm)
        else:
            self.logger.error('Not connected to database.')

    def delete(self, entity: Entity):
        if self.is_connected():
            stm = self._sql_factory\
                .delete(filters=SqlFilter({"UUID": '{}'.format(entity.uuid)}))\
                .replace(':tableName', self.table_name())
            self.logger.debug('Executing SQL statement: {}'.format(stm))
            self._cursor.execute(stm)

    def find_all(self, column_set: List[str] = None, sql_filters: SqlFilter = None) -> Optional[list]:
        if self.is_connected():
            stm = self._sql_factory\
                .select(column_set=column_set, filters=sql_filters)\
                .replace(':tableName', self.table_name())
            self.logger.debug('Executing SQL statement: {}'.format(stm))
            self._cursor.execute(stm)
            result = self._cursor.fetchall()
            return list(map(self.row_to_entity, result)) if result else None
        else:
            self.logger.error('Not connected to database.')

    def find_by_id(self, column_set: List[str] = None, entity_id: str = None) -> Optional[Entity]:
        if self.is_connected():
            if entity_id:
                stm = self._sql_factory\
                    .select(column_set=column_set, filters=SqlFilter({"UUID": '{}'.format(entity_id)}))\
                    .replace(':tableName', self.table_name())
                self.logger.debug('Executing SQL statement: {}'.format(stm))
                self._cursor.execute(stm)
                result = self._cursor.fetchall()
                if len(result) > 1:
                    raise ProgrammingError('Multiple results found')
                return self.row_to_entity(result[0]) if len(result) > 0 else None
            else:
                return None
        else:
            self.logger.error('Not connected to database.')

    def execute(self, sql_statement: str, auto_commit: bool = True, *params):
        if self.is_connected():
            self._cursor.execute(sql_statement, params)
            self.logger.debug('Executing SQL statement: {}'.format(sql_statement))
            if auto_commit:
                self.commit()
        else:
            self.logger.error('Not connected to database.')

    def commit(self):
        self.logger.debug('Committing database changes')
        self._connector.commit()

    def rollback(self):
        self.logger.debug('Rolling back database changes')
        self._connector.rollback()

    @abstractmethod
    def row_to_entity(self, row: Tuple) -> Entity:
        pass

    @abstractmethod
    def table_name(self) -> str:
        pass
