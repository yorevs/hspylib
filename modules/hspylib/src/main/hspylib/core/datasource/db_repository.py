#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.crud.db
      @file: db_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import contextlib
from abc import abstractmethod
from typing import Tuple, Any, TypeVar, Optional, Iterable

from retry import retry

from hspylib.core.datasource.crud_entity import CrudEntity
from hspylib.core.datasource.crud_repository import CrudRepository
from hspylib.core.datasource.db_configuration import DBConfiguration

Connection = TypeVar('Connection', bound=Any)
Cursor = TypeVar('Cursor', bound=Any)
Session = TypeVar('Session', bound=Any)
ResultSet = TypeVar('ResultSet', bound=Iterable)
T = TypeVar('T', bound=CrudEntity)


class DBRepository(CrudRepository[T]):
    """TODO"""

    def __init__(self, config: DBConfiguration):
        super().__init__()
        self._config = config

    def __str__(self):
        return f"{self.logname}/{self.table_name()} -> {self.info}"

    def __repr__(self):
        return str(self)

    @property
    def config(self) -> DBConfiguration:
        return self._config

    @property
    def info(self) -> str:
        return f"{self.username or ''}@{self.hostname or ''}:{self.port or 0}/{self.database or ''}"

    @property
    def hostname(self) -> str:
        return self._config.hostname

    @property
    def port(self) -> int:
        return self._config.port

    @property
    def username(self) -> str:
        return self._config.username

    @property
    def password(self) -> str:
        return self._config.password

    @property
    def database(self) -> str:
        return self._config.database

    @abstractmethod
    @retry(tries=3, delay=2, backoff=3, max_delay=30)
    def _create_session(self) -> Tuple[Connection, Cursor]:
        """TODO"""

    @abstractmethod
    @contextlib.contextmanager
    def _session(self) -> Session:
        """Create a database session."""

    @abstractmethod
    def execute(self, sql_statement: str, **kwargs) -> Tuple[int, Optional[ResultSet]]:
        """Execute a SQL statement."""

    @abstractmethod
    def table_name(self) -> str:
        """TODO"""
