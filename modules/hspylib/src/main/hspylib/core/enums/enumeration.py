#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.enum
      @file: enumeration.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from enum import Enum
from hspylib.core.preconditions import check_not_none
from typing import Any, List, Tuple, TypeVar

E = TypeVar("E", bound="Enumeration")


class Enumeration(Enum):
    """Extended enumeration type"""

    @classmethod
    def names(cls) -> List[str]:
        """Return all enumeration names"""
        return list(map(lambda e: e.name, cls))

    @classmethod
    def values(cls) -> List[Any]:
        """Return all enumeration values"""
        return list(map(lambda e: e.value, cls))

    @classmethod
    def value_of(cls, name: str, ignore_case: bool = True) -> E:
        """Create an enumeration provided it's matching name."""
        if ignore_case:
            found = next(filter(lambda en: en.name.upper() == name.upper(), list(cls)), None)
        else:
            found = next(filter(lambda en: en.name == name, list(cls)), None)
        return check_not_none(found, '"{}" name does not correspond to a valid "{}" enum', name, cls.__name__)

    @classmethod
    def of_value(cls, value: Any, ignore_case: bool = False) -> E:
        if ignore_case:
            found = next(filter(lambda en: str(en.value).upper() == str(value).upper(), list(cls)), None)
        else:
            found = next(filter(lambda en: en.value == value, list(cls)), None)
        return check_not_none(found, '"{}" value does not correspond to a valid "{}" enum', value, cls.__name__)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.name

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other: E) -> bool:
        if isinstance(other, self.__class__):
            return self.key == other.key
        return NotImplemented

    @property
    def key(self) -> Tuple[str, Any]:
        return self.name, self.value
