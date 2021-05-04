#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.test.hspylib.core.crud.resources
      @file: TestMysqlRepository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Tuple

from test.hspylib.core.crud.resources.TestEntity import TestEntity

from hspylib.core.crud.db.mysql.mysql_repository import MySqlRepository
from hspylib.core.tools.commons import get_or_default, str_to_bool


class TestMysqlRepository(MySqlRepository):
    def __init__(self):
        super().__init__()

    def row_to_entity(self, row: Tuple) -> TestEntity:
        return TestEntity(
            get_or_default(row, 0),
            get_or_default(row, 1),
            get_or_default(row, 2),
            str_to_bool(get_or_default(row, 3)))

    def table_name(self) -> str:
        return 'TEST'
