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
from typing import Any, Dict, Iterator, List, Optional, Tuple

from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.dict_tools import merge


class Namespace:

    @staticmethod
    def of(type_name: str, attributes: Dict[str, Any] | Tuple[Dict[str, Any]] | List[Dict[str, Any]]) -> 'Namespace':
        check_not_none(attributes)
        self = Namespace(type_name)
        self += attributes if isinstance(attributes, dict) else merge(attributes)
        return self

    def __init__(self, type_name: str = '', **kwargs) -> None:
        self.__name__ = type_name
        self._index = 0
        list(map(self.setattr, kwargs.keys(), kwargs.values()))

    def key(self) -> Tuple[Any]:
        return tuple(self.values)

    def __str__(self) -> str:
        return f"{self.__name__}({', '.join([f'{a}={av}' for a, av in zip(self.attributes, self.values)])})"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.key())

    def __eq__(self, other: 'Namespace') -> bool:
        if isinstance(other, self.__class__):
            return self.key() == other.key()
        return NotImplemented

    def __getitem__(self, attribute_name: str) -> Any:
        return getattr(self, attribute_name)

    def __len__(self) -> int:
        return len(self.attributes)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        self._index = 0
        return self

    def __next__(self) -> Tuple[str, Any]:
        if self._index < len(self):
            item = self.at(self._index)
            self._index += 1
            return item
        raise StopIteration

    def __contains__(self, attribute: str):
        return hasattr(self, attribute)

    def __iadd__(self, attribute: Dict[str, Any] | 'Namespace') -> 'Namespace':
        for a, av in attribute.items():
            self.setattr(a, av)
        return self

    def __add__(self, other: Dict[str, Any] | 'Namespace') -> 'Namespace':
        self.__name__ += '.' + other.__name__
        return self.__iadd__(other)

    def setattr(self, name: str, value: Any) -> 'Namespace':
        if name.startswith(('_', '__')):
            raise NameError("Attribute names can't start with '_' or '__'")
        setattr(self, name, value)
        return self

    def at(self, index: int) -> Optional[Tuple[str, Any]]:
        return (self.attributes[index], self.values[index]) if index < len(self) else None

    def items(self) -> Iterator[Tuple[str, Any]]:
        return iter(self)

    @property
    def attributes(self) -> Tuple[str]:
        attrs = list(filter(lambda name: self[name] is not None and not name.startswith(('_', '__')), vars(self)))
        return tuple(a for a in attrs)

    @property
    def values(self) -> Tuple[Any]:
        return tuple(filter(lambda v: v is not None, [getattr(self, a) for a in self.attributes]))
