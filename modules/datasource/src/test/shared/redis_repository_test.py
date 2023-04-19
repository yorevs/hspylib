#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: test.shared
      @file: sqlite_repository_test.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
import ast
from hspylib.core.enums.charset import Charset

from datasource.identity import Identity
from datasource.redis.redis_repository import RedisRepository
from shared.entity_test import EntityTest


class RedisRepositoryTest(RedisRepository[EntityTest]):
    def table_name(self) -> str:
        return "ENTITY_TEST"

    def build_key(self, entity: EntityTest) -> str:
        return entity.key()

    def to_entity_type(self, entity_string: bytes) -> EntityTest:
        entity_dict = ast.literal_eval(str(entity_string, encoding=Charset.UTF_8.val))
        identity = Identity(EntityTest.EntityId(entity_dict["id"]))
        return EntityTest(
            identity,
            id=entity_dict["id"],
            comment=entity_dict["comment"],
            lucky_number=entity_dict["lucky_number"],
            is_working=entity_dict["is_working"],
        )
