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

   Copyright 2021, HSPyLib team
"""

from abc import abstractmethod
from typing import Tuple

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.crud.crud_entity import CrudEntity
from hspylib.core.crud.crud_repository import CrudRepository


class DBRepository(CrudRepository):
    """TODO"""

    def __init__(self):
        super().__init__()
        self.hostname = AppConfigs.INSTANCE['datasource.hostname']
        self.port = AppConfigs.INSTANCE.get_int('datasource.port')
        self.user = AppConfigs.INSTANCE['datasource.username']
        self.password = AppConfigs.INSTANCE['datasource.password']
        self.database = AppConfigs.INSTANCE['datasource.database']

    def __str__(self):
        return f"{self.user}@{self.hostname}:{self.port}/{self.database}"

    @abstractmethod
    def connect(self):
        """TODO"""

    @abstractmethod
    def disconnect(self):
        """TODO"""

    @abstractmethod
    def is_connected(self):
        """TODO"""

    @abstractmethod
    def execute(self, sql_statement: str, auto_commit: bool, *params):
        """TODO"""

    @abstractmethod
    def commit(self):
        """TODO"""

    @abstractmethod
    def rollback(self):
        """TODO"""

    @abstractmethod
    def row_to_entity(self, row: Tuple) -> CrudEntity:
        """TODO"""

    @abstractmethod
    def table_name(self) -> str:
        """TODO"""
