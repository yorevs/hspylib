#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib
   @package: hspylib.main.hspylib.core.tools
      @file: collection_filter.py
   @created: Wed, 8 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import get_args, List, Set, TypeVar, Union

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.preconditions import check_argument
from hspylib.core.tools.text_tools import quote

T = TypeVar('T')
FILTER_VALUE = TypeVar('FILTER_VALUE', int, str, bool, float)


class FilterConditions(Enumeration):
    """TODO"""

    # @formatter:off
    LESS_THAN                   =      '<', Union[int, float]
    LESS_THAN_OR_EQUALS_TO      =     '<=', Union[int, float]
    GREATER_THAN                =      '>', Union[int, float]
    GREATER_THAN_OR_EQUALS_TO   =     '>=', Union[int, float]
    EQUALS_TO                   =     '==', Union[str, int, bool, float]
    DIFFERENT_FROM              =     '!=', Union[str, int, bool, float]
    CONTAINS                    =     'in', Union[str]
    DOES_NOT_CONTAIN            = 'not in', Union[str]
    IS                          =     '==', Union[bool]
    IS_NOT                      =     '!=', Union[bool]
    # @formatter:on

    def __str__(self):
        return self.name.lower().replace('_', ' ')

    def __repr__(self):
        return str(self)

    def matches(self, param_value: FILTER_VALUE, value: FILTER_VALUE) -> bool:
        """TODO"""
        return self._has_type(value) \
               and (
                   eval(f'{quote(value)} {self.value[0]} {quote(param_value)}')
                   if self.name in ['CONTAINS', 'DOES_NOT_CONTAIN']
                   else eval(f'{param_value} {self.value[0]} {value}')
               )

    def _has_type(self, value: FILTER_VALUE) -> bool:
        """TODO"""
        try:
            return isinstance(value, self.value[1])
        except TypeError:
            return isinstance(value, get_args(self.value[1]))


class ElementFilter:

    def __init__(
        self, name: str,
        el_name: str,
        condition: 'FilterConditions',
        el_value: FILTER_VALUE):
        self.name = name
        self.el_name = el_name
        self.condition = condition
        self.el_value = el_value

    def __str__(self):
        return f'{quote(self.el_name)} {self.condition} {quote(self.el_value)}'

    def __repr__(self):
        return str(self)

    def matches(self, element: T) -> bool:
        """TODO"""
        try:
            entry = element if isinstance(element, dict) else element.__dict__
            return self.el_name in entry \
                   and self.condition.matches(entry[self.el_name], self.el_value)
        except (NameError, TypeError, AttributeError):
            return False


class CollectionFilter:
    """TODO"""

    def __init__(self):
        self._filters: Set[ElementFilter] = set()

    def __str__(self):
        if len(self._filters) > 0:
            return ' '.join([f"{'AND ' if i > 0 else ''}{str(f)}" for i, f in enumerate(self._filters)])

        return 'No filters applied'

    def __repr__(self):
        return str(self)

    def __iter__(self):
        """Returns the Iterator object"""
        return self._filters.__iter__()

    def apply_filter(
        self,
        name: str,
        el_name: str,
        condition: 'FilterConditions',
        el_value: Union[int, str, bool, float]) -> None:
        """TODO"""

        check_argument(not any(f.name == name for f in self._filters),
                       f'Filter {name} already exists!')
        # Avoid applying the same filter
        if not any(
                f.el_name == el_name
                and f.condition == condition
                and f.el_value == el_value for f in self._filters):
            self._filters.add(ElementFilter(name, el_name, condition, el_value))

    def clear(self) -> None:
        """TODO"""
        self._filters.clear()

    def discard(self, name: str):
        """TODO"""
        element = next((e for e in self._filters if e.name == name), None)
        self._filters.discard(element)

    def filter(self, data: List[T]) -> List[T]:
        """TODO"""
        filtered: List[T] = []
        for element in data:
            if not self.should_filter(element):
                filtered.append(element)
        return filtered

    def filter_inverse(self, data: List[T]) -> List[T]:
        """TODO"""
        filtered: List[T] = []
        for element in data:
            if self.should_filter(element):
                filtered.append(element)
        return filtered

    def should_filter(self, data: T) -> bool:
        """TODO"""
        return not all(f.matches(data) for f in self._filters)
