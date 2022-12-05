#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.datasource.resources
      @file: firebase_repository_test.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.tools.dict_tools import get_or_default

from datasource.firebase.firebase_repository import FirebaseRepository
from datasource.identity import Identity
from shared.entity_test import EntityTest


class FirebaseRepositoryTest(FirebaseRepository[EntityTest]):

    def table_name(self) -> str:
        return 'hspylib-test.integration-test'

    def to_entity_type(self, entity_dict: dict | tuple) -> EntityTest:
        if isinstance(entity_dict, dict):
            identity = Identity(EntityTest.EntityId(entity_dict['id']))
            return EntityTest(identity, **entity_dict)

        identity = Identity(EntityTest.EntityId(entity_dict[0]))
        return EntityTest(
            identity,
            id=get_or_default(entity_dict, 0),
            comment=get_or_default(entity_dict, 1),
            lucky_number=get_or_default(entity_dict, 2),
            is_working=get_or_default(entity_dict, 3)
        )
