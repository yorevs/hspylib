#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Datasource
   @package: datasource
      @file: identity.py
   @created: Thu, 03 Nov 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import random
import string
import sys
from collections import namedtuple
from typing import Any, Dict, Tuple, Type, Union
from uuid import UUID, uuid4

from hspylib.core.namespace import Namespace
from hspylib.core.preconditions import check_argument

IDENTITY = Union[Tuple, int, str, UUID]


class Identity(Namespace):
    """TODO"""

    @classmethod
    def auto(cls, field_name: str = "id", id_type: Type = UUID) -> "Identity":
        _id_ = namedtuple("Identity", [f"{field_name}"])
        match id_type.__name__:
            case "int":
                number = random.randint(0, sys.maxsize)
                return Identity(_id_(number))
            case "str":
                letters = string.ascii_lowercase + "-_"
                st = "".join(random.choice(letters) for _ in range(32))
                return Identity(_id_(st))
            case "UUID":
                return Identity(_id_(uuid4().hex))
            case other:
                raise NotImplementedError(f"auto-identity generator for type '{other}' is not implemented")

    def __init__(self, identity: Tuple | Namespace | "Identity"):
        check_argument(isinstance(identity, Tuple | Identity | Namespace), "Must be a named tuple or Identity")
        identity = identity.identity if isinstance(identity, Identity) else identity
        self._identity = identity
        super().__init__("Identity", **self._asdict())

    def __str__(self) -> str:
        return str(self._identity)

    @property
    def identity(self) -> Tuple:
        return self._identity

    def _asdict(self) -> Dict[str, Any]:
        return self._identity._asdict()

    def as_column_set(self, separator: str = ",") -> str:
        """TODO"""
        column_set = []
        list(map(lambda key, value: column_set.append(f"{key} = {value}"), self.attributes, self.values))
        return separator.join(column_set)


if __name__ == "__main__":
    PersonId = namedtuple("PersonId", ["uuid"])
    UserId = namedtuple("UserId", ["uid", "email"])
    ns = Namespace(uuid=uuid4().hex)
    i1 = Identity.auto("uid")
    i2 = Identity(i1)
    i3 = Identity(UserId("12345", "user@example.com"))
    i4 = Identity(PersonId(uuid4().hex))
    i5 = Identity(ns)
    print("Identities: ", i1, i2, i3, i4, i5)
    print("Values: ", i1.values, i2.values, i3.values, i4.values, i5.values)
    print("Items: ", i1.items(), i2.items(), i3.items(), i4.items(), i5.items())
    print("Attrs/Values: ", i1.attributes, i1.values)
    print("Attrs/Values: ", i2.attributes, i2.values)
    print("Attrs/Values: ", i3.attributes, i3.values)
    print("Attrs/Values: ", i4.attributes, i4.values)
    print("Attrs/Values: ", i5.attributes, i5.values)
    print("As Dict: ", i1._asdict(), i2._asdict(), i3._asdict(), i4._asdict(), i5._asdict())
    print("As ColSet: ", i1.as_column_set(), i2.as_column_set(), i3.as_column_set(), i4.as_column_set(),
          i5.as_column_set())
