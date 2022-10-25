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
from typing import Any, Iterable, List, Tuple


class Namespace:

    def __init__(self, type_name: str, *args, **kwargs) -> None:
        self.__name__ = type_name
        list(map(self.set_attributes, filter(lambda a: isinstance(a, dict), args)))
        list(map(self.set_attribute, kwargs.keys(), kwargs.values()))

    def __str__(self) -> str:
        return f"{self.__name__}({', '.join([f'{a}={v}' for a, v in zip(self.attributes, self.values)])})"

    def __repr__(self) -> str:
        return str(self)

    def __key(self) -> Tuple:
        return tuple(self.values)

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other: 'Namespace') -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return NotImplemented

    def __getitem__(self, attribute_name: str):
        return getattr(self, attribute_name)

    def __iter__(self) -> Iterable:
        return iter([{k: v} for k, v in zip(self.attributes, self.values)])

    def __next__(self):
        return next(self.__iter__())

    @property
    def dict(self):
        return {k: self[k] for k in self.attributes}

    @property
    def attributes(self) -> List[str]:
        return [a for a in list(filter(lambda v: not v.startswith(('_', '__')), vars(self)))]

    @property
    def values(self) -> List[Any]:
        return [getattr(self, a) for a in self.attributes]

    def set_attributes(self, attributes: dict) -> 'Namespace':
        for k, v in attributes.items():
            self.set_attribute(k, v)
        return self

    def set_attribute(self, attribute_name: str, attribute_value: Any) -> 'Namespace':
        setattr(self, attribute_name, attribute_value)
        return self

    def get_attribute(self, attribute_name: str) -> 'Namespace':
        getattr(self, attribute_name)
        return self
