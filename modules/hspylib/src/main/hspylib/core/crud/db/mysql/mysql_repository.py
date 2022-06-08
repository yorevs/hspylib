#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.crud.db.mysql
      @file: mysql_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import logging as log
import uuid
from abc import abstractmethod
from typing import List, Optional, Tuple

import pymysql
from pymysql.err import OperationalError, ProgrammingError
from requests.structures import CaseInsensitiveDict as SqlFilter

from hspylib.core.crud.crud_entity import CrudEntity
from hspylib.core.crud.db.db_repository import DBRepository
from hspylib.core.crud.db.sql_factory import SqlFactory
from hspylib.core.exception.exceptions import NotConnectedError


class MySqlRepository(DBRepository):
    """TODO"""

    _connection_cache = {}

    def __init__(self):
        super().__init__()
        self._connector = None
        self._cursor = None
        self._sql_factory = SqlFactory()

    def is_connected(self) -> bool:
        """TODO"""
        return self._connector is not None

    def connect(self) -> None:
        """TODO"""
        if not self.is_connected():
            cache_key = self.__str__()
            if cache_key in self._connection_cache:
                self._connector = self._connection_cache[cache_key]
                self._cursor = self._connector.cursor()
                if not self.is_connected():
                    raise ConnectionError("Not connected to the database")
            else:
                db_url = f"{self.user}@{self.hostname}:{self.port}/{self.database}"
                try:
                    self._connector = pymysql.connect(
                        host=self.hostname,
                        user=self.user,
                        port=self.port,
                        password=self.password,
                        database=self.database)
                    if not self.is_connected():
                        raise ConnectionError(f"Unable to connect to {db_url}")
                    self._cursor = self._connector.cursor()
                    log.debug("Connection to %s established", db_url)
                    self._connection_cache[cache_key] = self._connector
                except (OperationalError, ConnectionRefusedError) as err:
                    raise ConnectionError(f"Unable to connect to {db_url}") from err

    def disconnect(self) -> None:
        """TODO"""
        if self.is_connected():
            cache_key = self.__str__()
            self._connector.close()
            del self._connector
            del self._connection_cache[cache_key]
            log.debug('Disconnected from %s', str(self))
        else:
            raise NotConnectedError('Not connected to database.')

    def insert(self, entity: CrudEntity) -> None:
        """TODO"""
        if self.is_connected():
            entity.uuid = entity.uuid if entity.uuid is not None else str(uuid.uuid4())
            stm = self._sql_factory \
                .insert(entity) \
                .replace(':tableName', self.table_name())
            log.debug("Executing SQL statement: %s", stm)
            self.execute(stm, True)
        else:
            raise NotConnectedError('Not connected to database.')

    def update(self, entity: CrudEntity) -> None:
        """TODO"""
        if self.is_connected():
            stm = self._sql_factory \
                .update(entity, filters=SqlFilter({"UUID": f'{entity.uuid}'})) \
                .replace(':tableName', self.table_name())
            log.debug('Executing SQL statement: %s', stm)
            self.execute(stm, True)
        else:
            raise NotConnectedError('Not connected to database.')

    def delete(self, entity: CrudEntity) -> None:
        """TODO"""
        if self.is_connected():
            stm = self._sql_factory \
                .delete(filters=SqlFilter({"UUID": f'{entity.uuid}'})) \
                .replace(':tableName', self.table_name())
            log.debug('Executing SQL statement: %s', stm)
            self.execute(stm, True)
        else:
            raise NotConnectedError('Not connected to database.')

    def find_all(  # pylint: disable=arguments-differ
        self,
        column_set: List[str] = None,
        sql_filters: SqlFilter = None) -> Optional[list]:
        """TODO"""

        if self.is_connected():
            stm = self._sql_factory \
                .select(column_set=column_set, filters=sql_filters) \
                .replace(':tableName', self.table_name())
            log.debug('Executing SQL statement: %s', stm)
            self.execute(stm, True)
            result = self._cursor.fetchall()
            return list(map(self.row_to_entity, result)) if result else None

        raise NotConnectedError('Not connected to database.')

    def find_by_id(  # pylint: disable=arguments-differ
        self,
        column_set: List[str] = None,
        entity_id: str = None) -> Optional[CrudEntity]:
        """TODO"""

        if self.is_connected():
            if entity_id:
                stm = self._sql_factory \
                    .select(column_set=column_set, filters=SqlFilter({"UUID": f'{entity_id}'})) \
                    .replace(':tableName', self.table_name())
                log.debug('Executing SQL statement: %s', stm)
                self.execute(stm, True)
                result = self._cursor.fetchall()
                if len(result) > 1:
                    raise ProgrammingError(f'Multiple results found {len(result)}')
                return self.row_to_entity(result[0]) if len(result) > 0 else None
            return None

        raise NotConnectedError('Not connected to database.')

    def execute(self, sql_statement: str, auto_commit: bool, *params) -> None:
        """TODO"""
        if self.is_connected():
            log.debug("Executing SQL statement: %s with params: [%s]", sql_statement, ', '.join(params))
            self._cursor.execute(sql_statement, *params)
            if auto_commit:
                self.commit()
        else:
            raise NotConnectedError('Not connected to database.')

    def commit(self) -> None:
        """TODO"""
        log.debug('Committing database changes')
        self._connector.commit()

    def rollback(self) -> None:
        """TODO"""
        log.debug('Rolling back database changes')
        self._connector.rollback()

    @abstractmethod
    def row_to_entity(self, row: Tuple) -> CrudEntity:
        pass

    @abstractmethod
    def table_name(self) -> str:
        pass
