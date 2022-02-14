#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.crud.resources
      @file: entity_test.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from uuid import UUID

from core.crud.crud_entity import CrudEntity


class EntityTest(CrudEntity):
    def __init__(self, entity_id: UUID = None, comment: str = None, lucky_number: int = 0, is_working: bool = False):
        super().__init__(entity_id)
        self.comment = comment
        self.lucky_number = lucky_number
        self.is_working = is_working

    def __str__(self):
        return 'uuid={} comment={} lucky_number={}'.format(self.uuid, self.comment, self.lucky_number)
