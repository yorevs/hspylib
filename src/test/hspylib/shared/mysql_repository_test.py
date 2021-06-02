#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.test.hspylib.core.crud.resources
      @file: mysql_repository_test.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Tuple

from test.hspylib.shared.entity_test import EntityTest

from hspylib.core.crud.db.mysql.mysql_repository import MySqlRepository
from hspylib.core.tools.commons import get_or_default, str_to_bool


class MysqlRepositoryTest(MySqlRepository):

    def row_to_entity(self, row: Tuple) -> EntityTest:
        return EntityTest(
            get_or_default(row, 0),
            get_or_default(row, 1),
            get_or_default(row, 2),
            str_to_bool(get_or_default(row, 3)))

    def table_name(self) -> str:
        return 'TEST'
