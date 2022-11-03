#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.tools
      @file: namespace.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Any, List, Tuple, Iterator, Optional, Dict, TypeVar

from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.dict_tools import merge_iterables

A = TypeVar('A', bound=str)
AV = TypeVar('AV', bound=Any)


class Namespace:

    @staticmethod
    def of(type_name: str, attributes: Dict[A, AV] | Tuple[Dict[A, AV]] | List[Dict[A, AV]]) -> 'Namespace':
        check_not_none(attributes)
        self = Namespace(type_name)
        self += attributes if isinstance(attributes, dict) else merge_iterables(attributes)
        return self

    def __init__(self, type_name: str, **kwargs) -> None:
        self.__name__ = type_name
        self._index = 0
        list(map(self.setattr, kwargs.keys(), kwargs.values()))

    def __key(self) -> Tuple[AV]:
        return tuple(self.values)

    def __str__(self) -> str:
        return f"{self.__name__}({', '.join([f'{a}={av}' for a, av in zip(self.attributes, self.values)])})"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other: 'Namespace') -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return NotImplemented

    def __getitem__(self, attribute_name: str) -> AV:
        return getattr(self, attribute_name)

    def __len__(self):
        return len(self.attributes)

    def __iter__(self) -> Iterator[Tuple[A, AV]]:
        self._index = 0
        return self

    def __next__(self) -> Tuple[A, AV]:
        if self._index < len(self):
            item = self.at(self._index)
            self._index += 1
            return item
        raise StopIteration

    def __contains__(self, attribute: A):
        return hasattr(self, attribute)

    def __iadd__(self, attribute: Dict[A, AV] | 'Namespace') -> 'Namespace':
        for a, av in attribute.items():
            self.setattr(a, av)
        return self

    def __add__(self, other: Dict[A, AV] | 'Namespace') -> 'Namespace':
        self.__name__ += '.' + other.__name__
        return self.__iadd__(other)

    def setattr(self, name: str, value: Any) -> 'Namespace':
        if name.startswith(('_', '__')):
            raise NameError("Attribute names can't start with '_' or '__'")
        setattr(self, name, value)
        return self

    def at(self, index: int) -> Optional[Tuple[A, AV]]:
        return (self.attributes[index], self.values[index]) if index < len(self) else None

    def items(self) -> Iterator[Tuple[A, AV]]:
        return iter(self)

    @property
    def attributes(self) -> List[A]:
        return [a for a in list(filter(lambda av: not av.startswith(('_', '__')), vars(self)))]

    @property
    def values(self) -> List[AV]:
        return [getattr(self, a) for a in self.attributes]
