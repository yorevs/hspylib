#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.test.hspylib.core.crud.resources
      @file: TestFileDbRepository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.core.crud.file.file_repository import FileRepository
from test.hspylib.core.crud.resources.TestEntity import TestEntity

class TestFileDbRepository(FileRepository):
    def __init__(self, filename: str):
        super().__init__(filename)

    def dict_to_entity(self, row: dict) -> TestEntity:
        return TestEntity(row['uuid'], row['comment'], row['lucky_number'], row['is_working'])

