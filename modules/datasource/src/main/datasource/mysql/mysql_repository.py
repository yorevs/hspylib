#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: datasource.mysql
      @file: mysql_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import contextlib
import logging as log
from typing import Generic, List, Optional, Set, Tuple, TypeVar

import pymysql
from hspylib.core.metaclass.singleton import AbstractSingleton
from hspylib.core.namespace import Namespace
from hspylib.core.tools.text_tools import quote
from pymysql import Connection, Error
from pymysql.cursors import Cursor
from retry import retry

from datasource.crud_entity import CrudEntity
from datasource.db_configuration import DBConfiguration
from datasource.db_repository import DBRepository, ResultSet, Session
from datasource.exception.exceptions import DatabaseConnectionError, DatabaseError
from datasource.identity import Identity

E = TypeVar("E", bound=CrudEntity)


class MySqlRepository(Generic[E], DBRepository[E, DBConfiguration], metaclass=AbstractSingleton):
    """Implementation of a data access layer for a MySql persistence store."""

    def __init__(self, config: DBConfiguration):
        super().__init__(config)

    @retry(tries=3, delay=2, backoff=3, max_delay=30)
    def _create_session(self) -> Tuple[Connection, Cursor]:
        log.debug("%s Attempt to connect to database: %s", self.logname, str(self))
        conn = pymysql.connect(
            host=self.hostname, user=self.username, port=self.port, password=self.password, database=self.database
        )
        return conn, conn.cursor()

    @contextlib.contextmanager
    def _session(self) -> Session:
        conn, dbs = None, None
        try:
            conn, dbs = self._create_session()
            log.debug("%s Successfully connected to database: %s [ssid=%d]", self.logname, self.info, hash(dbs))
            yield dbs
        except Error as err:
            raise DatabaseConnectionError(f"Unable to open/execute-on database session => {err}") from err
        finally:
            if conn:
                log.debug("%s Closing connection [ssid=%d]", self.logname, hash(dbs))
                conn.commit()
                conn.close()

    def execute(self, sql_statement: str, **kwargs) -> Tuple[int, Optional[ResultSet]]:
        """TODO"""
        with self._session() as dbs:
            try:
                rows = []
                log.debug(
                    f"{self.logname} Executing SQL statement {sql_statement} [ssid={hash(dbs)}]:\n"
                    f"\t|-Arguments: {str([f'{k}={v}' for k, v in kwargs.items()])}\n"
                    f"\t|-Statement: {sql_statement}"
                )
                if (rows_affected := dbs.execute(sql_statement, **kwargs) or 0) > 0:
                    list(map(rows.append, dbs))
                return rows_affected, rows
            except (pymysql.err.ProgrammingError, pymysql.err.OperationalError) as err:
                raise DatabaseError(f"Unable to execute statement => {sql_statement}") from err

    def count(self) -> int:
        sql = f"SELECT COUNT(*) FROM {self.table_name()}"
        return int(self.execute(sql)[1][0][0])

    def delete(self, entity: CrudEntity) -> None:
        self.delete_by_id(entity.identity)

    def delete_by_id(self, entity_id: Identity) -> None:
        clauses = [f"{k} = {quote(v)}" for k, v in zip(entity_id.attributes, entity_id.values)]
        sql = f"DELETE FROM {self.table_name()} WHERE " + " AND ".join(clauses)
        self.execute(sql)

    def delete_all(self, entities: List[E]) -> None:
        values, s = [], entities[0]
        list(map(lambda e: values.append(str(e.values)), entities))
        sql = f"DELETE FROM " f"{self.table_name()} WHERE ({s.as_columns()}) IN ({', '.join(values)}) "
        self.execute(sql)

    def save(self, entity: E) -> None:
        columns, ids = entity.as_columns(), set(entity.identity.attributes)
        sql = (
            f"INSERT INTO "
            f"{self.table_name()} ({columns}) VALUES {entity.values} AS new "
            f"ON DUPLICATE KEY UPDATE {entity.as_column_set(prefix='new.', exclude=ids)}"
        )
        self.execute(sql)

    def save_all(self, entities: List[E]) -> None:
        values, sample = [], entities[0]
        columns, ids = sample.as_columns(), set(sample.identity.attributes)
        list(map(lambda e: values.append(str(e.values)), entities))
        sql = (
            f"INSERT INTO "
            f"{self.table_name()} ({columns}) VALUES {', '.join(values)} AS new "
            f"ON DUPLICATE KEY UPDATE {sample.as_column_set(prefix='new.', exclude=ids)}"
        )
        self.execute(sql)

    def find_all(
        self,
        fields: Optional[Set[str]] = None,
        filters: Optional[Namespace] = None,
        order_bys: Optional[List[str]] = None,
        limit: int = 500,
        offset: int = 0,
    ) -> List[E]:

        fields = "*" if not fields else ", ".join(fields)
        clauses = list(filter(None, filters.values)) if filters else None
        orders = list(filter(None, order_bys)) if order_bys else None
        sql = (
            f"SELECT {fields} FROM {self.table_name()} "
            f"{('WHERE ' + ' AND '.join(clauses)) if clauses else ''} "
            f"{('ORDER BY ' + ', '.join(orders)) if orders else ''} "
            f"LIMIT {limit} OFFSET {offset}"
        )

        return list(map(self.to_entity_type, self.execute(sql)[1]))

    def find_by_id(self, entity_id: Identity, fields: Optional[Set[str]] = None) -> Optional[E]:

        fields = "*" if not fields else ", ".join(fields)
        clauses = [f"{k} = {quote(v)}" for k, v in zip(entity_id.attributes, entity_id.values)]
        sql = f"SELECT {fields} FROM {self.table_name()} " f"WHERE {' AND '.join(clauses)}"
        result = next((e for e in self.execute(sql)[1]), None)

        return self.to_entity_type(result) if result else None

    def exists_by_id(self, entity_id: Identity) -> bool:
        clauses = [f"{k} = {quote(v)}" for k, v in zip(entity_id.attributes, entity_id.values)]
        sql = f"SELECT EXISTS(SELECT 1 FROM {self.table_name()} WHERE {' AND '.join(clauses)})"

        return self.execute(sql)[1][0][0] > 0
