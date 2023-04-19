#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Datasource
   @package: test.shared
      @file: entity_test.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from collections import namedtuple
from hspylib.core.tools.commons import str_to_bool
from hspylib.core.tools.text_tools import snakecase
from typing import List

from datasource.crud_entity import CrudEntity
from datasource.identity import Identity


class EntityTest(CrudEntity):

    EntityId = namedtuple("EntityId", ["id"])

    @staticmethod
    def columns() -> List[str]:
        return ["id", "comment", "lucky_number", "is_working"]

    @classmethod
    def from_tuple(cls, values: tuple) -> "EntityTest":
        return EntityTest(Identity(cls.EntityId(values[0])), **{k: v for k, v in zip(cls.columns(), values)})

    def __init__(self, entity_id: Identity, **kwargs):
        self.id = None  # Will be filled later
        super().__init__(entity_id)
        self.comment = kwargs["comment"]
        self.lucky_number = kwargs["lucky_number"]
        self.is_working = str_to_bool(str(kwargs["is_working"]))

    def __str__(self) -> str:
        return f"id={self.id} comment={self.comment} lucky_number={self.lucky_number} working={self.is_working}"

    def key(self) -> str:
        return (
            snakecase(self.__class__.__name__, screaming=True)
            + "_"
            + self.identity.as_column_set().replace(" ", "").replace("=", "_").upper()
        )


if __name__ == "__main__":
    t1 = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
    t2 = EntityTest(Identity.auto(), comment="My-Test Data 2", lucky_number=55, is_working=False)
    print(t1, t1.values)
    print(t2, t2.values)
    print(t1.key(), t2.key())
