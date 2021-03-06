#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.test.hspylib.core.crud.resources
      @file: file_db_repository_test.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from test.hspylib.shared.entity_test import EntityTest

from hspylib.core.crud.file.file_repository import FileRepository


class FileDbRepositoryTest(FileRepository):

    def dict_to_entity(self, row: dict) -> EntityTest:
        return EntityTest(row['uuid'], row['comment'], row['lucky_number'], row['is_working'])
