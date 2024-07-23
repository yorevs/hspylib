#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: test.shared
      @file: cassandra_repository_test.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from datasource.cassandra.cassandra_repository import CassandraRepository
from datasource.identity import Identity
from shared.entity_test import EntityTest
from typing import NamedTuple


class CassandraRepositoryTest(CassandraRepository):
    def table_name(self) -> str:
        return "ENTITY_TEST"

    def to_entity_type(self, entity_tuple: NamedTuple) -> EntityTest:
        identity = Identity(EntityTest.EntityId(entity_tuple.id))
        return EntityTest(
            identity,
            id=entity_tuple.id,
            comment=entity_tuple.comment,
            lucky_number=entity_tuple.lucky_number,
            is_working=entity_tuple.is_working,
        )
