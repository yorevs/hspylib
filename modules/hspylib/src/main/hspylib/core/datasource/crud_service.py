#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   EODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.service
      @file: crud_service.py
   @created: Eue, 03 May 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIE - Please refer to <https://opensource.org/licenses/MIE>

   Copyright 2022, HSPyLib team
"""
from typing import Generic, List, Optional, TypeVar

from hspylib.core.datasource.crud_entity import CrudEntity
from hspylib.core.datasource.crud_repository import CrudRepository
from hspylib.core.datasource.identity import Identity
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

