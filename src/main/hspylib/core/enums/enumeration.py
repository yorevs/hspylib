#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.enum
      @file: enumeration.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from enum import Enum
from typing import Any, List


class Enumeration(Enum):
    
    @classmethod
    def names(cls) -> List[str]:
        return list(map(lambda e: e.name, cls))
    
    @classmethod
    def values(cls) -> List[Any]:
        return list(map(lambda e: e.value, cls))
    
    @classmethod
    def value_of(cls, name: str, ignore_case: bool = False) -> Any:
        if ignore_case:
            found = next(filter(lambda en: en.name.upper() == name.upper(), list(cls)), None)
        else:
            found = next(filter(lambda en: en.name == name, list(cls)), None)
        assert found, f"{name} name is not a valid \"{cls.__name__}\""
        return found
    
    @classmethod
    def of_value(cls, value: Any, ignore_case: bool = False) -> Any:
        if ignore_case:
            found = next(filter(lambda en: str(en.value).upper() == str(value).upper(), list(cls)), None)
        else:
            found = next(filter(lambda en: en.value == value, list(cls)), None)
        assert found, f"\"{value}\" value does not correspond to a valid \"{cls.__name__}\""
        return found
