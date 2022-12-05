#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: datasource
      @file: crud_service.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Generic, List, Optional, TypeVar

from datasource.crud_entity import CrudEntity
from datasource.crud_repository import CrudRepository
from datasource.identity import Identity
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.namespace import Namespace

E = TypeVar('E', bound=CrudEntity)
R = TypeVar('R', bound=CrudRepository)


class CrudService(Generic[R, E], metaclass=Singleton):

    def __init__(self, repository: R):
        self._repository = repository

    @property
    def repository(self) -> R:
        return self._repository

    def list(self, filters: Optional[Namespace] = None, order_bys: Optional[List[str]] = None) -> List[E]:
        return self.repository.find_all(filters=filters, order_bys=order_bys)

    def remove(self, entity: E) -> None:
        self.repository.delete(entity)

    def get(self, identity: Identity) -> Optional[E]:
        return self.repository.find_by_id(identity)

    def save(self, entity: E) -> None:
        self.repository.save(entity)
