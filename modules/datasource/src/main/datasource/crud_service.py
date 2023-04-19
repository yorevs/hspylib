#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: datasource
      @file: crud_service.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from datasource.crud_entity import CrudEntity
from datasource.crud_repository import CrudRepository
from datasource.identity import Identity
from hspylib.core.metaclass.singleton import AbstractSingleton
from hspylib.core.namespace import Namespace
from typing import Generic, List, Optional, Set, TypeVar

E = TypeVar("E", bound=CrudEntity)
R = TypeVar("R", bound=CrudRepository)


class CrudService(Generic[R, E], metaclass=AbstractSingleton):
    """Provide a service for CRUD operations."""

    def __init__(self, repository: R):
        self._repository = repository

    @property
    def repository(self) -> R:
        return self._repository

    def list(self, filters: Namespace | None = None, order_bys: Set[str] | None = None) -> List[E]:
        """Return a list of all entries matching filters.
        :param filters: entry filters.
        :param order_bys: result set order bys.
        """
        return self.repository.find_all(filters=filters, order_bys=order_bys) or []

    def remove(self, entity: E) -> None:
        """Removes the specified entity.
        :param entity: the entity to delete.
        """
        self.repository.delete(entity)

    def get(self, identity: Identity) -> Optional[E]:
        """Gets the entity specified by ID."""
        return self.repository.find_by_id(identity)

    def save(self, entity: E) -> None:
        """Saves the specified entity.
        :param entity: the entity to save.
        """
        self.repository.save(entity)
