#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.crud.file
      @file: file_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import contextlib
import logging as log
import sqlite3
from sqlite3 import Error
from typing import List, Optional, Tuple, Iterable, Set, TypeVar

from hspylib.core.datasource.crud_entity import CrudEntity
from hspylib.core.datasource.db_repository import Session, DBRepository, ResultSet, Connection, Cursor
from hspylib.core.datasource.identity import Identity
from hspylib.core.datasource.sqlite.sqlite_configuration import SQLiteConfiguration
from hspylib.core.exception.exceptions import DatabaseConnectionError, DatabaseError
from hspylib.core.tools.namespace import Namespace
from hspylib.core.tools.text_tools import quote

T = TypeVar('T', bound=CrudEntity)


class SQLiteRepository(DBRepository[T]):
    """Implementation of a data access layer for a SQLite persistence store."""

    def __init__(self, config: SQLiteConfiguration):
        super().__init__(config)

    @property
    def db_file(self) -> str:
        return self._config.db_file

    @property
    def info(self) -> str:
        return f"{self.db_file}"

    def _create_session(self) -> Tuple[Connection, Cursor]:
        log.debug(f"{self.logname} Attempt to connect to database: {str(self)}")
        conn = sqlite3.connect(self.db_file)
        return conn, conn.cursor()

    @contextlib.contextmanager
    def _session(self) -> Session:
        log.debug(f"{self.logname} Attempt to connect to database: {str(self)}")
        conn, dbs = None, None
        try:
            conn, dbs = self._create_session()
            log.debug(f"{self.logname} Successfully connected to database: {self.info} [{self.db_file}]")
            yield dbs
        except Error as err:
            raise DatabaseConnectionError(f"Unable to open/execute-on database session => {err}") from err
        finally:
            if conn:
                log.debug(f"{self.logname} Closing connection [ssid={self.db_file}]")
                conn.commit()
                conn.close()

    def execute(self, sql_statement: str, **kwargs) -> Tuple[int, Optional[ResultSet]]:
        """TODO"""
        with self._session() as dbs:
            try:
                log.debug(f"{self.logname} Executing SQL statement {sql_statement} [ssid={hash(dbs)}]:\n"
                          f"\t|-Arguments: {str([f'{k}={v}' for k, v in kwargs.items()])}\n"
                          f"\t|-Statement: {sql_statement}")
                rows = dbs.execute(sql_statement, **kwargs).fetchall()
                return len(rows), rows
            except (sqlite3.ProgrammingError, sqlite3.OperationalError) as err:
                raise DatabaseError(f"Unable to execute statement => {sql_statement}") from err

    def count(self) -> int:
        sql = f"SELECT COUNT(*) FROM {self.table_name()}"
        return int(self.execute(sql)[1][0][0])

    def delete(self, entity: T) -> None:
        self.delete_by_id(entity.identity)

    def delete_by_id(self, entity_id: Identity) -> None:
        clauses = [f"{k} = {quote(v)}" for k, v in zip(entity_id.attributes, entity_id.values)]
        sql = f"DELETE FROM {self.table_name()} WHERE " + ' AND '.join(clauses)
        self.execute(sql)

    def delete_all(self, entities: List[T]) -> None:
        values, s = [], entities[0]
        list(map(lambda e: values.append(str(e.values)), entities))
        sql = f"DELETE FROM " \
              f"{self.table_name()} WHERE ({s.as_columns()}) IN ({', '.join(values)}) "
        self.execute(sql)

    def save(self, entity: T, exclude_update: Iterable[str] = None) -> None:
        sql = f"INSERT INTO " \
              f"{self.table_name()} ({entity.as_columns()}) VALUES {entity.values} " \
              f"ON CONFLICT DO UPDATE SET {entity.as_column_set(prefix='EXCLUDED.', exclude=exclude_update)}"
        self.execute(sql)

    def save_all(self, entities: List[T], exclude_update: Iterable[str] = None) -> None:
        values, s = [], entities[0]
        list(map(lambda e: values.append(str(e.values)), entities))
        sql = f"INSERT INTO " \
              f"{self.table_name()} ({s.as_columns()}) VALUES {', '.join(values)} " \
              f"ON CONFLICT DO UPDATE SET {s.as_column_set(prefix='EXCLUDED.', exclude=exclude_update)}"
        self.execute(sql)

    def find_all(
        self,
        fields: Set[str] = None,
        filters: Namespace = None,
        limit: int = 500, offset: int = 0) -> List[T]:

        fields = '*' if not fields else ', '.join(fields)
        clauses = filter(None, [f for f in filters.values]) if filters else None
        sql = f"SELECT {fields} FROM {self.table_name()} {'WHERE ' + ' AND '.join(clauses) if clauses else ''} " \
              f"LIMIT {limit} OFFSET {offset}"

        return list(map(self.to_entity_type, self.execute(sql)[1]))

    def find_by_id(self, entity_id: Identity, fields: Set[str] = None) -> Optional[T]:
        fields = '*' if not fields else ', '.join(fields)
        clauses = [f"{k} = {quote(v)}" for k, v in zip(entity_id.attributes, entity_id.values)]
        sql = f"SELECT {fields} FROM {self.table_name()} WHERE " + ' AND '.join(clauses)
        result = next((e for e in self.execute(sql)[1]), None)

        return self.to_entity_type(result) if result else None

    def exists_by_id(self, entity_id: Identity) -> bool:
        clauses = [f"{k} = {quote(v)}" for k, v in zip(entity_id.attributes, entity_id.values)]
        sql = f"SELECT EXISTS(SELECT 1 FROM {self.table_name()} WHERE " + ' AND '.join(clauses) + ")"

        return self.execute(sql)[1][0][0] > 0
