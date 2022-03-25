#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.model
      @file: crud_entity.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import json
from abc import ABC
from typing import Tuple
from uuid import UUID


class CrudEntity(ABC):
    """TODO"""

    def __init__(self, entity_id: UUID = None):
        self.uuid = entity_id

    def __str__(self):
        return f"{self.__class__.__name__}:{str(self.to_dict())}"

    def __eq__(self, other):
        return isinstance(other, CrudEntity) \
               and all(item in self.to_dict().items() for item in other.to_dict().items())

    def to_dict(self) -> dict:
        """TODO"""

        ret_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, bool):
                ret_dict[key] = bool(value)
            elif isinstance(value, int):
                ret_dict[key] = int(value)
            elif isinstance(value, float):
                ret_dict[key] = float(value)
            elif isinstance(value, (str, UUID)):
                ret_dict[key] = str(value)
            else:
                ret_dict[key] = value.__dict__() if value else {}
        return ret_dict

    def to_json(self) -> str:
        """TODO"""
        dict_obj = self.to_dict()
        json_str = json.dumps(dict_obj)
        return json_str

    def to_columns(self) -> Tuple[str]:
        """TODO"""
        cols = []
        for key in self.__dict__:
            if not key.startswith('_'):
                cols.append(key.replace("'", "").upper())
        return tuple(cols)

    def to_column_set(self) -> dict:
        """TODO"""
        fields = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                fields[key.replace("'", "").upper()] = f"{str(value)}"
        return fields

    def to_values(self) -> Tuple[str]:
        """TODO"""
        values = []
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                values.append(str(value))
        return tuple(values)
