#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: hspylib
   @package: hspylib.core
      @file: collection_filter.py
   @created: Wed, 8 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import get_args, Iterable, Iterator, Set, Tuple, TypeVar, Union

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.preconditions import check_argument
from hspylib.core.tools.text_tools import quote

T = TypeVar("T")
FILTER_VALUE = TypeVar("FILTER_VALUE", int, str, bool, float)


class FilterCondition(Enumeration):
    """Collection filter conditions."""

    # fmt: off
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
    # fmt: on

    def __str__(self) -> str:
        return self.name.lower().replace("_", " ")

    def __repr__(self) -> str:
        return str(self)

    def matches(self, param_value: FILTER_VALUE, value: FILTER_VALUE) -> bool:
        """Whether this filter value matches the specified param."""
        operator = self.value[0]
        if self.name in ["CONTAINS", "DOES_NOT_CONTAIN"]:
            expression = f"{quote(value)} {operator} {quote(param_value)}"
        else:
            expression = f"{quote(param_value)} {operator} {quote(value)}"
        return self._allow_type(value) and eval(expression)  # pylint: disable=eval-used

    def _allow_type(self, value: FILTER_VALUE) -> bool:
        """Whether this filter condition allows the specified value type."""
        try:
            return isinstance(value, self.value[1])
        except TypeError:
            return isinstance(value, get_args(self.value[1]))


class ElementFilter:
    """Represent a single filter condition."""

    def __init__(self, name: str, el_name: str, condition: "FilterCondition", el_value: FILTER_VALUE):
        self.name = name
        self.el_name = el_name
        self.condition = condition
        self.el_value = el_value

    def __str__(self):
        return f"{quote(self.el_name)} {self.condition} {quote(self.el_value)}"

    def __repr__(self):
        return str(self)

    def key(self) -> Tuple[str, "FilterCondition", FILTER_VALUE]:
        return self.el_name, self.condition, self.el_value

    def __hash__(self) -> int:
        return hash(self.key())

    def __eq__(self, other: "ElementFilter") -> bool:
        if isinstance(other, self.__class__):
            return self.key() == other.key()
        return NotImplemented

    def matches(self, element: T) -> bool:
        """Whether this filter is True for the given element."""

        try:
            entry = None
            if isinstance(element, dict):
                entry = element
            elif hasattr(element, "__dict__"):
                entry = element.__dict__
            elif isinstance(element, tuple):
                entry = dict(element)
            return self.el_name in entry and self.condition.matches(entry[self.el_name], self.el_value)
        except (NameError, TypeError, AttributeError):
            return False


class CollectionFilter:
    """A collection of filters to be applied to a given iterable."""

    def __init__(self) -> None:
        self._filters: Set[ElementFilter] = set()

    def __str__(self) -> str:
        if len(self._filters) > 0:
            return " ".join([f"{'AND ' if i > 0 else ''}{str(f)}" for i, f in enumerate(self._filters)])
        return "No filters applied"

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self) -> Iterator:
        return self._filters.__iter__()

    def __len__(self) -> int:
        return len(self._filters)

    def apply_filter(
        self, name: str, el_name: str, condition: "FilterCondition", el_value: Union[int, str, bool, float]
    ) -> None:
        """Apply the specified filter."""

        check_argument(not any(f.name == name for f in self._filters), f"Filter {name} already exists!")
        f = ElementFilter(name, el_name, condition, el_value)
        self._filters.add(f)

    def clear(self) -> None:
        """Clear all filters."""
        self._filters.clear()

    def discard(self, name: str):
        """Discard the specified filter."""
        element = next((e for e in self._filters if e.name == name), None)
        self._filters.discard(element)

    def filter(self, data: Iterable[T]) -> Iterable[T]:
        """Filter the collection."""
        filtered: Iterable[T] = data.__class__()
        for element in data:
            if not self.should_filter(element):
                if hasattr(filtered, "append"):
                    filtered.append(element)
                elif hasattr(filtered, "add"):
                    filtered.add(element)
        return filtered

    def filter_inverse(self, data: Iterable[T]) -> Iterable[T]:
        """Inverse filter the collection."""
        filtered: Iterable[T] = data.__class__()
        for element in data:
            if self.should_filter(element):
                if hasattr(filtered, "append"):
                    filtered.append(element)
                elif hasattr(filtered, "add"):
                    filtered.add(element)
        return filtered

    def should_filter(self, data: T) -> bool:
        """Whether the specified data should be filtered, according to this filter collection."""
        return not all(f.matches(data) for f in self._filters)
