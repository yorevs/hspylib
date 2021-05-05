#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.test.hspylib.core.crud.resources
      @file: firebase_repository_test.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.core.crud.db.firebase.firebase_repository import FirebaseRepository
from hspylib.core.model.entity import Entity
from test.hspylib.shared.entity_test import EntityTest


class FirebaseRepositoryTest(FirebaseRepository):
    
    def row_to_entity(self, row: dict) -> Entity:
        return EntityTest(row['uuid'], row['comment'], row['lucky_number'], row['is_working'])
    
    def database_name(self) -> str:
        return 'hspylib'