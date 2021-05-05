#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.crud.db.mysql
      @file: mysql_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import uuid
from abc import abstractmethod
from typing import List, Optional, Tuple

import pymysql
from pymysql.err import OperationalError, ProgrammingError
from requests.structures import CaseInsensitiveDict as SqlFilter

from hspylib.core.crud.db.db_repository import DBRepository
from hspylib.core.crud.db.sql_factory import SqlFactory
from hspylib.core.exception.exceptions import NotConnectedError
from hspylib.core.model.entity import Entity


class MySqlRepository(DBRepository):
    _connections = {}
    
    def __init__(self):
        super().__init__()
        self._connector = None
        self._cursor = None
        self._sql_factory = SqlFactory()
    
    def is_connected(self) -> bool:
        return self._connector is not None
    
    def connect(self) -> None:
        if not self.is_connected():
            cache_key = self.__str__()
            if cache_key in MySqlRepository._connections:
                self._connector = MySqlRepository._connections[cache_key]
                self._cursor = self._connector.cursor()
                if not self.is_connected():
                    raise ConnectionError("Not connected to the database")
            else:
                try:
                    self._connector = pymysql.connect(
                        host=self.hostname,
                        user=self.user,
                        port=self.port,
                        password=self.password,
                        database=self.database
                    )
                    if not self.is_connected():
                        raise ConnectionError("Unable to connect to the database")
                    self._cursor = self._connector.cursor()
                    log.debug('Connection to {} established'.format(str(self)))
                    MySqlRepository._connections[cache_key] = self._connector
                except (OperationalError, ConnectionRefusedError) as err:
                    raise ConnectionError('Unable to connect to {}'.format(str(self))) from err

    def disconnect(self) -> None:
        if self.is_connected():
            cache_key = self.__str__()
            self._connector.close()
            self._connector = None
            del MySqlRepository._connections[cache_key]
            log.debug('Disconnected from {}.'.format(str(self)))
        else:
            raise NotConnectedError('Not connected to database.')
    
    def insert(self, entity: Entity) -> None:
        if self.is_connected():
            entity.uuid = entity.uuid if entity.uuid is not None else str(uuid.uuid4())
            stm = self._sql_factory \
                .insert(entity) \
                .replace(':tableName', self.table_name())
            log.debug(f"Executing SQL statement: {stm}")
            self.execute(stm, True)
        else:
            raise NotConnectedError('Not connected to database.')
    
    def update(self, entity: Entity) -> None:
        if self.is_connected():
            stm = self._sql_factory \
                .update(entity, filters=SqlFilter({"UUID": '{}'.format(entity.uuid)})) \
                .replace(':tableName', self.table_name())
            log.debug('Executing SQL statement: {}'.format(stm))
            self.execute(stm, True)
        else:
            raise NotConnectedError('Not connected to database.')
    
    def delete(self, entity: Entity) -> None:
        if self.is_connected():
            stm = self._sql_factory \
                .delete(filters=SqlFilter({"UUID": '{}'.format(entity.uuid)})) \
                .replace(':tableName', self.table_name())
            log.debug('Executing SQL statement: {}'.format(stm))
            self.execute(stm, True)
        else:
            raise NotConnectedError('Not connected to database.')
    
    def find_all(
            self,
            column_set: List[str] = None,
            sql_filters: SqlFilter = None) -> Optional[list]:
        
        if self.is_connected():
            stm = self._sql_factory \
                .select(column_set=column_set, filters=sql_filters) \
                .replace(':tableName', self.table_name())
            log.debug('Executing SQL statement: {}'.format(stm))
            self.execute(stm, True)
            result = self._cursor.fetchall()
            return list(map(self.row_to_entity, result)) if result else None

        raise NotConnectedError('Not connected to database.')
    
    def find_by_id(
            self,
            column_set: List[str] = None,
            entity_id: str = None) -> Optional[Entity]:
        
        if self.is_connected():
            if entity_id:
                stm = self._sql_factory \
                    .select(column_set=column_set, filters=SqlFilter({"UUID": '{}'.format(entity_id)})) \
                    .replace(':tableName', self.table_name())
                log.debug('Executing SQL statement: {}'.format(stm))
                self.execute(stm, True)
                result = self._cursor.fetchall()
                if len(result) > 1:
                    raise ProgrammingError(f'Multiple results found {len(result)}')
                return self.row_to_entity(result[0]) if len(result) > 0 else None
            return None

        raise NotConnectedError('Not connected to database.')
    
    def execute(self, sql_statement: str, auto_commit: bool, *params) -> None:
        if self.is_connected():
            log.debug(f"Executing SQL statement: {sql_statement} with params: [{', '.join(params)}]")
            self._cursor.execute(sql_statement, *params)
            if auto_commit:
                self.commit()
        else:
            raise NotConnectedError('Not connected to database.')
    
    def commit(self) -> None:
        log.debug('Committing database changes')
        self._connector.commit()
    
    def rollback(self) -> None:
        log.debug('Rolling back database changes')
        self._connector.rollback()
    
    @abstractmethod
    def row_to_entity(self, row: Tuple) -> Entity:
        pass
    
    @abstractmethod
    def table_name(self) -> str:
        pass
