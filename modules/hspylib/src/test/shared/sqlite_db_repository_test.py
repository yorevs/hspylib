#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.datasource.resources
      @file: sqlite_db_repository_test.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.core.datasource.identity import Identity
from hspylib.core.datasource.sqlite.sqlite_repository import SQLiteRepository

from shared.entity_test import EntityTest


class SQLiteRepositoryTest(SQLiteRepository[EntityTest]):

    def table_name(self) -> str:
        return 'ENTITY_TEST'

    def to_entity_type(self, entity_dict: dict | tuple) -> EntityTest:
        if isinstance(entity_dict, dict):
            identity = Identity(EntityTest.EntityId(entity_dict['id']))
            return EntityTest(identity, **entity_dict)

        identity = Identity(EntityTest.EntityId(entity_dict[0]))
        return EntityTest(
            identity, id=entity_dict[0], comment=entity_dict[1], lucky_number=entity_dict[2], is_working=entity_dict[3]
        )