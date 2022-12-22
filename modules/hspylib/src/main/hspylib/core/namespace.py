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

ATTRIBUTE_TYPES = Dict[str, Any] | Tuple[Dict[str, Any]] | List[Dict[str, Any]]


class Namespace:
    """TODO"""

    @staticmethod
    def of(type_name: str, attributes: ATTRIBUTE_TYPES, final: bool = False) -> "Namespace":
        check_not_none(attributes)
        self = Namespace(type_name, final)
        self += attributes if isinstance(attributes, dict) else merge(attributes)
        return self

    def __init__(self, type_name: str = None, final: bool = False, **kwargs) -> None:
        self.__name__ = type_name or self.__class__.__name__
        self._final = None
        self._index = 0
        list(map(self.setattr, kwargs.keys(), kwargs.values()))
        self._final = final

    @property
    def attributes(self) -> Tuple[str]:
        # fmt: off
        return tuple(
            attr for attr in filter(
                lambda name:
                    self[name] is not None
                    and not name.startswith(("_", "__"))
                    and not name.endswith(("_", "__")),
                vars(self),
            )
        )
        # fmt: on

    @property
    def values(self) -> Tuple[Any]:
        all_values = [self[attr] for attr in self.attributes]
        # fmt: off
        return tuple(
            filter(
                lambda val:
                    val is not None,
                all_values
            )
        )
        # fmt: on

    def __str__(self) -> str:
        return f"{self.__name__}({', '.join([f'{a}={av}' for a, av in zip(self.attributes, self.values)])})"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.key())

    def __eq__(self, other: "Namespace") -> bool:
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
            item = self.item_at(self._index)
            self._index += 1
            return item
        raise StopIteration

    def __contains__(self, *attributes: str):
        return all(hasattr(self, attr) for attr in attributes)

    def __iadd__(self, attribute: Dict[str, Any] | "Namespace") -> "Namespace":
        for a, av in attribute.items():
            self.setattr(a, av)
        return self

    def __add__(self, other: Dict[str, Any] | "Namespace") -> "Namespace":
        self.__name__ += "_" + other.__name__
        return self.__iadd__(other)

    def key(self) -> Tuple[Any]:
        return tuple(self.values)

    def setattr(self, name: str, value: Any) -> "Namespace":
        if self._final and not hasattr(self, name):
            raise ValueError(f"Can't set attribute '{name}'. '{self.__name__}' Namespace is final")
        if not not hasattr(self, name):
            self._check_name(name)
        setattr(self, name, value)
        return self

    def item_at(self, index: int) -> Optional[Tuple[str, Any]]:
        # fmt: off
        return (
            self.attributes[index], self.values[index]
        ) if index < len(self) \
          else None
        # fmt: on

    def items(self) -> Iterator[Tuple[str, Any]]:
        return iter(self)

    def hasattr(self, *names: str) -> bool:
        return self.__contains__(*names)

    def _asdict(self) -> Dict[str, Any]:
        """
        To match the same function name as namedtuple, we used _asdict
        """
        return dict(zip(self.attributes, self.values))

    def _check_name(self, name: str) -> None:
        # fmt: off
        if not (
            self.hasattr(name)
            or (
                not name.startswith(("_", "__"))
                and not name.endswith(("_", "__"))
                and name not in (forbidden := vars(self).keys())
            )
        ):
            raise NameError(
                f"Invalid attribute name '{name}'. "
                f"Attributes can't start with '_' or '__' and must not be in {forbidden}")
        # fmt: on
