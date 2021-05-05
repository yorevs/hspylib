#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.crud
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

ET = TypeVar('ET')
RT = TypeVar('RT')


class CrudService(Generic[ET, RT]):
    
    def __init__(self, repository: RT):
        self.repository = repository
    
    def save(self, entity: ET) -> None:
        if not self.get(entity.uuid):
            self.repository.insert(entity)
        else:
            self.repository.update(entity)
    
    def remove(self, entity: ET) -> None:
        if not self.get(entity.uuid):
            raise EntityNotFoundError(
                "{} was not found: {}".format(entity.__class__, entity))
        self.repository.delete(entity)
    
    def list(self, filters: str = None) -> List[ET]:
        ret_val = self.repository.find_all(filters)
        return ret_val if ret_val else []
    
    def get(self, uuid: UUID) -> Optional[ET]:
        return self.repository.find_by_id(str(uuid))
