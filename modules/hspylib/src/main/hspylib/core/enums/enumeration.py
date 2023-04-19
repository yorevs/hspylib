#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.enums
      @file: enumeration.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from enum import auto, Enum
from hspylib.core.preconditions import check_argument, check_not_none
from typing import Any, List, Tuple, TypeVar

E = TypeVar("E", bound="Enumeration")


def composable(cls: type):
    """Make the enumeration class, composable"""
    check_argument(issubclass(cls, Enumeration))
    setattr(cls.__class__, "_CUSTOM", auto())
    return cls


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

    @classmethod
    def compose(cls, first: E, *others: E) -> E:
        try:
            e = getattr(first.__class__, "_CUSTOM")
            e._value_ = str(first)  # pylint: disable=protected-access
            for other in others:
                e._value_ += str(other)
            return e
        except AttributeError as err:
            raise AttributeError("Composable enumerations must declare a '_CUSTOM' member") from err

    def __str__(self):
        return str(self._value_)

    def __repr__(self):
        return self.name

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other: E) -> bool:
        if isinstance(other, self.__class__):
            return self.key == other.key
        return NotImplemented

    def __add__(self, other) -> E:
        return Enumeration.compose(self, other)

    @property
    def key(self) -> Tuple[str, Any]:
        return self.name, self.value
