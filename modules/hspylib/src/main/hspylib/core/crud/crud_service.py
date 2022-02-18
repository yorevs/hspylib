#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.crud
      @file: crud_service.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from hspylib.core.exception.exceptions import EntityNotFoundError

E = TypeVar('E')
R = TypeVar('R')


class CrudService(Generic[E, R]):
    """TODO"""

    def __init__(self, repository: R):
        self.repository = repository

    def save(self, entity: E) -> None:
        """TODO"""
        if not self.get(entity.uuid):
            self.repository.insert(entity)
        else:
            self.repository.update(entity)

    def remove(self, entity: E) -> None:
        """TODO"""
        if not self.get(entity.uuid):
            raise EntityNotFoundError("{entity.__class__} was not found: {entity}")
        self.repository.delete(entity)

    def list(self, filters: str = None) -> List[E]:
        """TODO"""
        ret_val = self.repository.find_all(filters)
        return ret_val if ret_val else []

    def get(self, uuid: UUID) -> Optional[E]:
        """TODO"""
        return self.repository.find_by_id(str(uuid))
