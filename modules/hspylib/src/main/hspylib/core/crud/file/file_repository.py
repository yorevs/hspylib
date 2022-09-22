#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.crud.file
      @file: file_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import logging as log
import re
import uuid
from abc import abstractmethod
from typing import Any, List, Optional

from hspylib.core.crud.crud_entity import CrudEntity
from hspylib.core.crud.crud_repository import CrudRepository
from hspylib.core.crud.file.file_storage import FileStorage
from hspylib.core.exception.exceptions import ProgrammingError


class FileRepository(CrudRepository):
    """TODO"""

    _storages = {}

    @staticmethod
    def check_criteria(partial_value, whole_value) -> bool:
        """TODO
        :param partial_value:
        :param whole_value:
        :return:
        """
        if isinstance(whole_value, str):
            return str(partial_value).upper() in whole_value.upper()
        if isinstance(whole_value, int):
            return int(partial_value) == whole_value
        if isinstance(whole_value, float):
            return float(partial_value) == whole_value
        if isinstance(whole_value, bool):
            return bool(partial_value) == whole_value

        return False

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.storage = self.__get_storage()

    def __str__(self):
        return str(self.storage.data)

    def insert(self, entity: CrudEntity) -> None:
        """TODO
        :param entity:
        """
        entity.uuid = entity.uuid if entity.uuid else str(uuid.uuid4())
        self.storage.data.append(entity.to_dict())
        self.storage.commit()
        log.debug("%s has been inserted !", entity.__class__.__name__)

    def update(self, entity: CrudEntity) -> None:
        """TODO
        :param entity:
        """
        for index, next_entry in enumerate(self.storage.data):
            if next_entry['uuid'] == entity.uuid:
                self.storage.data[index] = entity.to_dict()
                self.storage.commit()
                log.debug("%s has been updated !", entity.__class__.__name__)

    def delete(self, entity: CrudEntity) -> None:
        """TODO
        :param entity:
        """
        for index, next_entry in enumerate(self.storage.data):
            if next_entry['uuid'] == entity.uuid:
                self.storage.data.remove(self.storage.data[index])
                self.storage.commit()
                log.debug("%s has been deleted !", entity.__class__.__name__)

    def find_all(self, filters: str = None) -> List[CrudEntity]:
        """TODO
        :param filters:
        """
        self.storage.load()
        if filters:
            file_filters = filters.split(',')
            filtered = []
            for next_filter in file_filters:
                fields = re.split('=|>|<|>=|<=|==|!=', next_filter)
                try:
                    found = [
                        self.dict_to_entity(data) for data in self.storage.data if
                        self.check_criteria(fields[1], data[fields[0]])
                    ]
                except KeyError:
                    continue  # Just skip the filter and continue
                except IndexError:
                    continue  # Just skip the filter and continue
                filtered.extend(found)
            return filtered

        return [self.dict_to_entity(data) for data in self.storage.data]

    def find_by_id(self, entity_id: uuid.UUID) -> Optional[CrudEntity]:
        """TODO
        :param entity_id:
        """
        self.storage.load()
        if entity_id:
            result = [data for data in self.storage.data if entity_id == data['uuid']]
            if len(result) > 1:
                raise ProgrammingError(f'Multiple results {len(result)} found with entity_id={entity_id}')
            return self.dict_to_entity(result[0]) if len(result) > 0 else None

        return None

    @abstractmethod
    def dict_to_entity(self, row: dict) -> CrudEntity:
        """TODO
        :param row:
        """

    def __get_storage(self) -> Any:
        """Create or get a storage according to the filename"""
        if self.filename in self._storages:
            return self._storages[self.filename]

        self._storages[self.filename] = FileStorage(self.filename)
        return self._storages[self.filename]
