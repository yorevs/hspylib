#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.test.hspylib.core.crud.resources
      @file: TestEntity.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from uuid import UUID
from hspylib.core.model.entity import Entity


class TestEntity(Entity):
    def __init__(self, entity_id: UUID = None, comment: str = None, lucky_number: int = 0, is_working: bool = False):
        super().__init__(entity_id)
        self.comment = comment
        self.lucky_number = lucky_number
        self.is_working = is_working

    def __str__(self):
        return 'uuid={} comment={} lucky_number={}'.format(self.uuid, self.comment, self.lucky_number)
