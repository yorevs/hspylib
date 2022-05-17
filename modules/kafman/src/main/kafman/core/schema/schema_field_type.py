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
    BOOLEAN         = 'boolean'  # A binary value
    INT             = 'int'      # 32-bit signed integer
    LONG            = 'long'     # 64-bit signed integer
    FLOAT           = 'float'    # Single precision (32-bit) IEEE 754 floating-point number
    DOUBLE          = 'double'   # Double precision (64-bit) IEEE 754 floating-point number
    BYTES           = 'bytes'    # Sequence of 8-bit unsigned bytes
    STRING          = 'string'   # Unicode character sequence
    RECORD          = 'record'   # Records use the type name "record"
    ENUM            = 'enum'     # Enums use the type name "enum"
    ARRAY           = 'array'    # Arrays use the type name "array"
    MAP             = 'map'      # Maps use the type name "map"
    UNION           = 'union'    # Unions, as mentioned above, are represented using JSON arrays
    FIXED           = 'fixed'    # Fixed uses the type name "fixed"
    # @formatter:on

    @classmethod
    def of_type(cls, r_type: Union[str, List[Union[str, dict]]]) -> 'SchemaFieldType':
        """TODO"""
        if isinstance(r_type, str):  # Primitive Types
            return SchemaFieldType.of_value(r_type)
        elif isinstance(r_type, dict):
            return SchemaFieldType.of_value(r_type['type'])
        else:  # Complex Types
            c_type = next((x['type'] if isinstance(x, dict) else x for x in r_type if x != 'null'), None)
            return SchemaFieldType.of_value(c_type)

    def empty_value(self) -> Any:
        """TODO"""
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

    def is_primitive(self):
        return self.value not in ['record', 'enum', 'array', 'map', 'union', 'fixed']

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
