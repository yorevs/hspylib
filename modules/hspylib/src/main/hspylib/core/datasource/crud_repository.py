#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.crud
      @file: crud_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import json
from abc import abstractmethod
from typing import Iterable, List, Optional, Set, Generic, TypeVar

from hspylib.core.datasource.crud_entity import CrudEntity
from hspylib.core.datasource.identity import Identity
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.namespace import Namespace

T = TypeVar('T', bound=CrudEntity)


class CrudRepository(Generic[T], metaclass=Singleton):
    """Interface for generic CRUD operations on a repository for a specific type."""

    @property
    def logname(self) -> str:
        """TODO"""
        return self.__class__.__name__.split('_')[0]

    @abstractmethod
    def count(self) -> int:
        """TODO"""

    @abstractmethod
    def delete(self, entity: T) -> None:
        """TODO"""

    @abstractmethod
    def delete_by_id(self, entity_id: Identity) -> None:
        """TODO"""

    @abstractmethod
    def delete_all(self, entities: List[T]) -> None:
        """TODO"""

    @abstractmethod
    def save(self, entity: T, exclude_update: Iterable[str] = None) -> None:
        """TODO"""

    @abstractmethod
    def save_all(self, entities: List[T], exclude_update: Iterable[str] = None) -> None:
        """TODO"""

    @abstractmethod
    def find_all(
        self,
        fields: Set[str] = None,
        filters: Namespace = None,
        limit: int = 500, offset: int = 0) -> List[T]:
        """TODO"""

    @abstractmethod
    def find_by_id(self, entity_id: Identity, fields: Set[str] = None) -> Optional[T]:
        """TODO"""

    def exists_by_id(self, entity_id: Identity) -> bool:
        """TODO"""

    @abstractmethod
    def to_entity_type(self, entity_dict: dict | tuple) -> T:
        """TODO"""

    def to_entity_list(self, json_string: str, filters: Namespace = None) -> List[T]:
        """Return filtered entries from the json_string as a list"""
        ret_list = []
        for value in json.loads(json_string).values():
            if not filters or all(k in value and value[k] == v for k, v in filters.items()):
                ret_list.append(self.to_entity_type(value))
        return ret_list
