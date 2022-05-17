#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: schema_field_type.py
   @created: Fri, 01 Apr 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from typing import Any, List, Union

from hspylib.core.enums.enumeration import Enumeration


class SchemaFieldType(Enumeration):
    """TODO"""

    # @formatter:off
    BOOLEAN         = 'boolean'
    INT             = 'int'
    LONG            = 'long'
    FLOAT           = 'float'
    DOUBLE          = 'double'
    BYTES           = 'bytes'
    STRING          = 'string'
    RECORD          = 'record'
    ENUM            = 'enum'
    ARRAY           = 'array'
    MAP             = 'map'
    FIXED           = 'fixed'
    COMPLEX         = 'complex'
    # @formatter:on

    @classmethod
    def of_type(cls, r_type: Union[str, List[Union[str, dict]]]) -> 'SchemaFieldType':
        if isinstance(r_type, str):
            return SchemaFieldType.of_value(r_type)
        else:
            c_type = next(
                (x for x in r_type if cls.is_simple_type(x)),
                'record' if 'record' in r_type else 'complex')
            return SchemaFieldType.of_value(c_type)

    @classmethod
    def is_simple_type(cls, type_str: str):
        return type_str not in ['complex', 'record'] and type_str in SchemaFieldType.values()

    def empty_value(self) -> Any:
        if self.value == 'boolean':
            return False
        elif self.value in ['int', 'long']:
            return 0
        elif self.value in ['float', 'double']:
            return 0.0
        elif self.value == 'bytes':
            return b''
        elif self.value == 'array':
            return []
        else:
            return ''

    def is_complex(self):
        return self.value == 'complex'

    def is_primitive(self):
        return self.value not in ['record', 'enum', 'array', 'map', 'fixed']

    def is_record(self):
        return self.value == 'record'

    def is_enum(self):
        return self.value == 'enum'

    def is_array(self):
        return self.value == 'array'

    def is_map(self):
        return self.value == 'map'

    def is_fixed(self):
        return self.value == 'fixed'

    def is_read_only(self):
        return self.value in ['record', 'fixed', 'complex']
