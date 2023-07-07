#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: datasource
      @file: crud_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from abc import abstractmethod
from datasource.crud_entity import CrudEntity
from datasource.identity import Identity
from hspylib.core.metaclass.singleton import AbstractSingleton
from hspylib.core.namespace import Namespace
from typing import Generic, List, Optional, Set, TypeVar

import json

E = TypeVar("E", bound=CrudEntity)


class CrudRepository(Generic[E], metaclass=AbstractSingleton):
    """Interface for generic CRUD operations on a repository for a specific type."""

    @property
    def logname(self) -> str:
        return self.__class__.__name__.split("_", maxsplit=1)[0]

    @abstractmethod
    def count(self) -> int:
        """Returns the number of entities available."""

    @abstractmethod
    def delete(self, entity: E) -> None:
        """Deletes a given entity.
        :param entity: the entity to delete.
        """

    @abstractmethod
    def delete_by_id(self, entity_id: Identity) -> None:
        """Deletes the entity with the given id.
        :param entity_id: the ID of the entity to be deleted.
        """

    @abstractmethod
    def delete_all(self, entities: List[E]) -> None:
        """Deletes all given entities.
        :param entities: the entities to be deleted.
        """

    @abstractmethod
    def save(self, entity: E) -> None:
        """Saves a given entity.
        :param entity: the entity to save.
        """

    @abstractmethod
    def save_all(self, entities: List[E]) -> None:
        """Saves all given entities.
        :param entities: the entities to be saved.
        """

    @abstractmethod
    def find_all(
        self,
        columns: Set[str] | None = None,
        filters: Namespace | None = None,
        order_bys: Set[str] | None = None,
        limit: int = 500,
        offset: int = 0,
    ) -> List[E]:
        """Returns all entities of the type.
        :param columns: the column names to select.
        :param filters: entry filters.
        :param order_bys: result set order bys.
        :param limit: the maximum number of entries to be fetch.
        :param offset: skip offset entries before fetch.
        """

    @abstractmethod
    def find_by_id(self, entity_id: Identity, columns: Set[str] | None = None) -> Optional[E]:
        """Retrieves an entity by its id.
        :param entity_id: the entity ID.
        :param columns: the column names to select.
        """

    def exists_by_id(self, entity_id: Identity) -> bool:
        """Returns whether an entity with the given id exists.
        :param entity_id: the entity ID.
        """

    @abstractmethod
    def to_entity_type(self, entity_dict: dict | tuple) -> E:
        """Convert a dict or tuple, generally from a result set, into the CRUD entity.
        :param entity_dict: the entity dict or tuple to be converted.
        """

    def to_entity_list(self, json_string: str, filters: Namespace | None = None) -> List[E]:
        """Return filtered entries from the json_string as a list.
        :param json_string: the json string to be parsed.
        :param filters: entry filters.
        """
        ret_list = []
        for value in json.loads(json_string).values():
            if not filters or all(k in value and value[k] == v for k, v in filters.items()):
                ret_list.append(self.to_entity_type(value))
        return ret_list
