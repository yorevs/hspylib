import sys
import uuid
from abc import abstractmethod
from typing import Optional

import pymysql as pymysql
from pymysql.err import OperationalError, ProgrammingError
from requests.structures import CaseInsensitiveDict

from main.hspylib.core.crud.db.db_repository import DBRepository
from main.hspylib.core.crud.db.sql_factory_facade import SqlFactoryFacade
from main.hspylib.core.enum.database_type import DatabaseType
from main.hspylib.core.model.entity import Entity


class MySqlRepository(DBRepository):
    __connections = {}

    def __init__(self):
        super().__init__()
        self.connector = None
        self.sql_factory = SqlFactoryFacade.get(DatabaseType.MYSQL)

    def __str__(self):
        return "{}@{}:{}/{}".format(self.user, self.hostname, self.port, self.database)

    def is_connected(self):
        return self.connector is not None

    def connect(self):
        if not self.is_connected():
            cache_key = self.__str__()
            if cache_key in MySqlRepository.__connections:
                self.connector = MySqlRepository.__connections[cache_key]
                self.cursor = self.connector.cursor()
                assert self.is_connected(), "Not connected to the database"
            else:
                try:
                    self.connector = pymysql.connect(
                        host=self.hostname,
                        user=self.user,
                        port=self.port,
                        password=self.password,
                        database=self.database
                    )
                    assert self.is_connected(), "Unable to connect to the database"
                    self.cursor = self.connector.cursor()
                    self.logger.debug('Connection to {} established'.format(str(self)))
                    MySqlRepository.__connections[cache_key] = self.connector
                except OperationalError:
                    self.logger.error('Unable to connect to {}'.format(str(self)))
                    sys.exit(1)

    def disconnect(self):
        if self.is_connected():
            self.connector.close()
            self.connector = None
            self.logger.debug('Disconnected from {}.'.format(str(self)))
        else:
            self.logger.error('Unable to disconnect from {}'.format(str(self)))
            sys.exit(1)

        return self.connector

    def insert(self, entity: Entity):
        entity.uuid = entity.uuid if entity.uuid is not None else str(uuid.uuid4())
        insert_stm = self.sql_factory.insert(entity)
        self.logger.debug('Executing SQL statement: {}'.format(insert_stm))
        self.cursor.execute(insert_stm)
        self.connector.commit()

    def update(self, entity: Entity):
        update_stm = self.sql_factory.update(entity, filters=CaseInsensitiveDict({
            "UUID": '{}'.format(entity.uuid)
        }))
        self.logger.debug('Executing SQL statement: {}'.format(update_stm))
        self.cursor.execute(update_stm)
        self.connector.commit()

    def delete(self, entity: Entity):
        delete_stm = self.sql_factory.delete(filters=CaseInsensitiveDict({
            "UUID": '{}'.format(entity.uuid)
        }))
        self.logger.debug('Executing SQL statement: {}'.format(delete_stm))
        self.cursor.execute(delete_stm)
        self.connector.commit()

    def find_all(self, sql_filters: CaseInsensitiveDict[str, str] = None) -> Optional[list]:
        select_stm = self.sql_factory.select(filters=sql_filters)
        self.logger.debug('Executing SQL statement: {}'.format(select_stm))
        try:
            self.cursor.execute(select_stm)
            result = self.cursor.fetchall()
            ret_val = []
            for next_row in result:
                ret_val.append(self.row_to_entity(next_row))
            return ret_val
        except ProgrammingError:
            return None

    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        if entity_id:
            select_stm = self.sql_factory.select(filters=CaseInsensitiveDict({
                "UUID": '{}'.format(entity_id)
            }))
            self.logger.debug('Executing SQL statement: {}'.format(select_stm))
            self.cursor.execute(select_stm)
            result = self.cursor.fetchall()
            return self.row_to_entity(result[0]) if len(result) > 0 else None
        else:
            return None

    @abstractmethod
    def row_to_entity(self, row: tuple) -> Entity:
        pass
