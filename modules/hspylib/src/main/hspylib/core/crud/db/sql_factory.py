#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.crud.db
      @file: sql_factory.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import logging as log
import os
from typing import List, Optional

from requests.structures import CaseInsensitiveDict

from hspylib.core.crud.crud_entity import CrudEntity
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.preconditions import check_argument, check_state


class SqlFactory(metaclass=Singleton):
    """TODO"""

    _DEFAULT_SQL_STUBS = f'{os.path.dirname(__file__)}/sql/sql_stubs.sql'

    @staticmethod
    def _read_stubs(sql_filename: str) -> dict:
        """TODO"""
        sql_stubs = {}
        check_argument(os.path.exists(sql_filename), "Sql file was not found: {}", sql_filename)
        with open(sql_filename, encoding='utf-8') as f_stubs:
            lines = f_stubs.readlines()
            check_state(len(lines) > 0, "SQL Stub file is empty")
            lines = list(map(str.strip, lines))
            stubs = ' '.join(lines).split(';')
            check_state(
                len(stubs) >= 4, "Stub file does not have the minimum stubs for [insert, select, update, delete]")
            for stub in stubs:
                if stub:
                    key = stub.strip().partition(' ')[0].lower()
                    sql_stubs[key] = stub.strip()
        return sql_stubs

    @staticmethod
    def _join_filters(filters: CaseInsensitiveDict, join_operator: str = 'AND') -> str:
        """TODO"""
        filter_string = ''
        if filters:
            for key, value in filters.items():
                filter_string += f"{join_operator} {key} = '{value}'"
        return filter_string

    @staticmethod
    def _join_fieldset(entity: CrudEntity) -> str:
        """TODO"""
        fields = entity.to_column_set()
        field_set = ''
        for key, value in fields.items():
            field_set += f"{', ' if field_set else ''}{key} = '{value}'"
        return field_set

    def __init__(self):
        self.sql_stubs = SqlFactory._read_stubs(self._DEFAULT_SQL_STUBS)
        log.debug('%s created with %s Stubs', self.__class__.__name__, len(self.sql_stubs))

    def insert(self, entity: CrudEntity) -> Optional[str]:
        """TODO"""
        params = entity.to_values()
        sql = self.sql_stubs['insert'] \
            .replace(':columnSet', str(entity.to_columns()).replace("'", "")) \
            .replace(':valueSet', str(params))
        return sql

    def select(self, column_set: List[str] = None, filters: CaseInsensitiveDict = None) -> Optional[str]:
        """TODO"""
        sql = self.sql_stubs['select'] \
            .replace(':columnSet', '*' if not column_set else ', '.join(column_set)) \
            .replace(':filters', SqlFactory._join_filters(filters))
        return sql

    def update(self, entity: CrudEntity, filters: CaseInsensitiveDict) -> Optional[str]:
        """TODO"""
        sql = self.sql_stubs['update'] \
            .replace(':fieldSet', SqlFactory._join_fieldset(entity)) \
            .replace(':filters', SqlFactory._join_filters(filters))
        return sql

    def delete(self, filters: CaseInsensitiveDict) -> Optional[str]:
        """TODO"""
        sql = self.sql_stubs['delete'] \
            .replace(':filters', SqlFactory._join_filters(filters))
        return sql
