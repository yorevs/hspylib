#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.crud.db
      @file: sql_factory.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import os
from typing import List, Optional

from requests.structures import CaseInsensitiveDict

from hspylib.core.meta.singleton import Singleton
from hspylib.core.model.entity import Entity

DEFAULT_SQL_STUBS = '{}/sql/sql_stubs.sql'.format(os.path.dirname(__file__))


class SqlFactory(metaclass=Singleton):
    
    @staticmethod
    def read_stubs(sql_filename: str) -> dict:
        ret_val = {}
        assert os.path.exists(sql_filename), "Sql file was not found: {}".format(sql_filename)
        with open(sql_filename) as f_stubs:
            lines = f_stubs.readlines()
            assert lines, "Stub file is empty"
            lines = list(map(str.strip, lines))
            stubs = ' '.join(lines).split(';')
            assert len(stubs) >= 4, "Stub file hasn't got the minimum stubs for [insert, select, update, delete]"
            for stub in stubs:
                if stub:
                    key = stub.strip().partition(' ')[0].lower()
                    ret_val[key] = stub.strip()
        return ret_val
    
    @staticmethod
    def join_filters(filters: CaseInsensitiveDict, join_operator: str = 'AND') -> str:
        filter_string = ''
        if filters:
            for key, value in filters.items():
                filter_string += "{} {} = '{}'".format(join_operator, key, value)
        return filter_string
    
    @staticmethod
    def join_fieldset(entity: Entity) -> str:
        fields = entity.to_column_set()
        field_set = ''
        for key, value in fields.items():
            field_set += "{}{} = '{}'".format(', ' if field_set else '', key, value)
        return field_set
    
    def __init__(self):
        self.sql_stubs = SqlFactory.read_stubs(DEFAULT_SQL_STUBS)
        log.debug('{} created with {} Stubs'.format(
            self.__class__.__name__,
            len(self.sql_stubs)))
    
    def insert(self, entity: Entity) -> Optional[str]:
        params = entity.to_values()
        sql = self.sql_stubs['insert'] \
            .replace(':columnSet', str(entity.to_columns()).replace("'", "")) \
            .replace(':valueSet', str(params))
        return sql
    
    def select(self, column_set: List[str] = None, filters: CaseInsensitiveDict = None) -> Optional[str]:
        sql = self.sql_stubs['select'] \
            .replace(':columnSet', '*' if not column_set else ', '.join(column_set)) \
            .replace(':filters', SqlFactory.join_filters(filters))
        return sql
    
    def update(self, entity: Entity, filters: CaseInsensitiveDict) -> Optional[str]:
        sql = self.sql_stubs['update'] \
            .replace(':fieldSet', SqlFactory.join_fieldset(entity)) \
            .replace(':filters', SqlFactory.join_filters(filters))
        return sql
    
    def delete(self, filters: CaseInsensitiveDict) -> Optional[str]:
        sql = self.sql_stubs['delete'] \
            .replace(':filters', SqlFactory.join_filters(filters))
        return sql
