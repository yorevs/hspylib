#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.service
      @file: crud_service.py
   @created: Tue, 03 May 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Optional, List, Generic, TypeVar

from hspylib.core.datasource.crud_entity import CrudEntity
from hspylib.core.datasource.crud_repository import CrudRepository
from hspylib.core.datasource.identity import Identity
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.namespace import Namespace

T = TypeVar('T', bound=CrudEntity)


class CrudService(Generic[T], metaclass=Singleton):

    def __init__(self, repository: CrudRepository):
        self._repository = repository

    @property
    def repository(self) -> CrudRepository:
        return self._repository

    def list(self, filters: Namespace = None) -> List[T]:
        return self.repository.find_all(filters=filters)

    def remove(self, entity: T) -> None:
        self.repository.delete(entity)

    def get(self, identity: Identity) -> Optional[T]:
        return self.repository.find_by_id(identity)

    def save(self, entity: T) -> None:
        self.repository.save(entity)

