#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: datasource.cassandra
      @file: cassandra_repository.py
   @created: Sat, 12 Nov 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import contextlib
import logging as log
from typing import Generic, List, Optional, Set, Tuple, TypeVar

from cassandra import UnresolvableContactPoints
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, NoHostAvailable
from hspylib.core.metaclass.singleton import AbstractSingleton
from hspylib.core.namespace import Namespace
from hspylib.core.tools.text_tools import quote
from retry import retry

from datasource.cassandra.cassandra_configuration import CassandraConfiguration
from datasource.crud_entity import CrudEntity
from datasource.db_repository import Connection, Cursor, DBRepository, ResultSet, Session
from datasource.exception.exceptions import DatabaseConnectionError, DatabaseError
from datasource.identity import Identity

E = TypeVar("E", bound=CrudEntity)


class CassandraRepository(Generic[E], DBRepository[E, CassandraConfiguration], metaclass=AbstractSingleton):
    """Implementation of a data access layer for a cassandra persistence store."""

    def __init__(self, config: CassandraConfiguration):
        super().__init__(config)

    @property
    def secure_bundle_path(self) -> str:
        return self._config.secure_bundle_path

    @property
    def protocol_version(self) -> int:
        return self._config.protocol_version

    @property
    def connect_timeout(self) -> int:
        return self._config.connect_timeout

    @property
    def default_timeout(self) -> int:
        return self._config.default_timeout

    @retry(tries=3, delay=2, backoff=3, max_delay=30)
    def _create_session(self) -> Tuple[Connection, Cursor]:
        log.debug("%s Attempt to connect to database: %s", self.logname, str(self))
        auth_provider = PlainTextAuthProvider(username=self.username, password=self.password)
        if self.secure_bundle_path:
            log.info("%s Using Astra Security Bundle: %s", self.logname, self.secure_bundle_path)
            cloud_config = {"secure_connect_bundle": self.secure_bundle_path}
            cursor = Cluster(protocol_version=self.protocol_version, auth_provider=auth_provider, cloud=cloud_config)
        else:
            log.info(
                f"{self.logname} Attempt to connect to Astra: "
                f"{self.username}@{self.hostname}:{self.port}/{self.database}"
            )
            cursor = Cluster(
                protocol_version=self.protocol_version,
                auth_provider=auth_provider,
                contact_points=[self.hostname],
                port=self.port,
            )
        session = cursor.connect()
        cursor.connect_timeout = self.connect_timeout
        session.default_timeout = self.default_timeout
        return cursor, session

    @contextlib.contextmanager
    def _session(self) -> Session:
        conn, dbs = None, None
        try:
            conn, dbs = self._create_session()
            log.debug("%s Successfully connected to database: %s [ssid=%d]", self.logname, self.info, hash(dbs))
            yield dbs
        except (UnresolvableContactPoints, NoHostAvailable) as err:
            raise DatabaseConnectionError(f"Unable to open/execute-on database session => {err}") from err
        finally:
            if conn:
                log.debug("%s Shutting down connection [ssid=%d]", self.logname, hash(dbs))
                conn.shutdown()

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
                rs = dbs.execute(sql_statement, **kwargs)
                if rs.current_rows:
                    list(map(rows.append, rs.current_rows))
                return len(rs.current_rows), rows
            except Exception as err:
                raise DatabaseError(f"Unable to execute statement => {sql_statement}") from err

    def count(self) -> int:
        sql = f"SELECT COUNT(*) FROM {self.table_name()}"
        return int(self.execute(sql)[1][0][0])

    def delete(self, entity: CrudEntity) -> None:
        self.delete_by_id(entity.identity)

    def delete_by_id(self, entity_id: Identity) -> None:
        clauses = [f"{k} = {quote(v)}" for k, v in zip(entity_id.attributes, entity_id.values)]
        sql = f"DELETE FROM {self.database}.{self.table_name()} WHERE " + " AND ".join(clauses)
        self.execute(sql)

    def delete_all(self, entities: List[E]) -> None:
        values, s = [], entities[0]
        list(map(lambda e: values.append(str(e.values)), entities))
        sql = f"DELETE FROM {self.database}.{self.table_name()} " f"WHERE ({s.as_columns()}) IN ({', '.join(values)}) "
        self.execute(sql)

    def save(self, entity: E) -> None:
        columns, _ = entity.as_columns(), set(entity.identity.attributes)
        sql = f"INSERT INTO {self.database}.{self.table_name()} " f"({columns}) VALUES {entity.values} "
        self.execute(sql)

    def save_all(self, entities: List[E]) -> None:
        values, sample, inserts = [], entities[0], []
        columns, _ = sample.as_columns(), set(sample.identity.attributes)
        list(map(lambda e: values.append(str(e.values)), entities))
        list(
            map(
                lambda v: inserts.append(f"INSERT INTO {self.database}.{self.table_name()} ({columns}) VALUES {v} "),
                values,
            )
        )
        sql = f"BEGIN BATCH " f"{'; '.join(inserts)} " f"APPLY BATCH;"
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
        orders = list(filter(None, order_bys)) if order_bys and clauses else None  # Order by require filters
        sql = (
            f"SELECT {fields} FROM {self.database}.{self.table_name()} "
            f"{('WHERE ' + ' AND '.join(clauses)) if clauses else ''} "
            f"{('ORDER BY ' + ', '.join(orders)) if orders else ''} "
            f"LIMIT {limit}"
        )

        return list(map(self.to_entity_type, self.execute(sql)[1]))

    def find_by_id(self, entity_id: Identity, fields: Optional[Set[str]] = None) -> Optional[E]:

        fields = "*" if not fields else ", ".join(fields)
        clauses = [f"{k} = {quote(v)}" for k, v in zip(entity_id.attributes, entity_id.values)]
        sql = f"SELECT {fields} FROM {self.database}.{self.table_name()} " f"WHERE {' AND '.join(clauses)}"
        result = next((e for e in self.execute(sql)[1]), None)

        return self.to_entity_type(result) if result else None

    def exists_by_id(self, entity_id: Identity) -> bool:
        clauses = [f"{k} = {quote(v)}" for k, v in zip(entity_id.attributes, entity_id.values)]
        sql = f"SELECT EXISTS(SELECT 1 FROM {self.table_name()} WHERE {' AND '.join(clauses)})"

        return self.execute(sql)[1][0][0] > 0
