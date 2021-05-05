#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.crud
      @file: crud_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from requests.structures import CaseInsensitiveDict

from hspylib.core.model.entity import Entity


class CrudRepository(ABC):
    @abstractmethod
    def insert(self, entity: Entity) -> None:
        pass
    
    @abstractmethod
    def update(self, entity: Entity) -> None:
        pass
    
    @abstractmethod
    def delete(self, entity: Entity) -> None:
        pass
    
    @abstractmethod
    def find_all(self, filters: CaseInsensitiveDict = None) -> List[Entity]:
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        pass
