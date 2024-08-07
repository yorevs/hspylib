#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: phonebook.entity
      @file: person.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from collections import namedtuple
from datasource.crud_entity import CrudEntity
from datasource.identity import Identity
from typing import List, Tuple


class Person(CrudEntity):
    PersonId = namedtuple("PersonId", ["uuid"])

    @staticmethod
    def columns() -> List[str]:
        return ["uuid", "email", "name", "age", "phone", "address", "complement"]

    @classmethod
    def from_tuple(cls, values: Tuple) -> "Person":
        row = {k: v for k, v in zip(cls.columns(), values)}
        return Person(Identity(cls.PersonId(row["uuid"])), **row)
