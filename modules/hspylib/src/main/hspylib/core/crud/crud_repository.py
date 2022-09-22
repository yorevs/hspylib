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

from abc import ABC, abstractmethod
from typing import List, Optional

from requests.structures import CaseInsensitiveDict

from hspylib.core.crud.crud_entity import CrudEntity


class CrudRepository(ABC):
    """TODO"""

    @abstractmethod
    def insert(self, entity: CrudEntity) -> None:
        """TODO
        param: entity
        """

    @abstractmethod
    def update(self, entity: CrudEntity) -> None:
        """TODO
        param: entity
        """

    @abstractmethod
    def delete(self, entity: CrudEntity) -> None:
        """TODO
        param: entity
        """

    @abstractmethod
    def find_all(self, filters: CaseInsensitiveDict = None) -> List[CrudEntity]:
        """TODO
        param: entity
        """

    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[CrudEntity]:
        """TODO
        param: entity
        """
