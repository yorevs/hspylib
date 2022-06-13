#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib-kafman
   @package: hspylib-kafman.main.kafman.core.schema.json
      @file: json_type.py
   @created: Wed, 8 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from collections import defaultdict
from typing import Any

from hspylib.core.enums.enumeration import Enumeration


class JsonType(Enumeration):
    """TODO"""

    # @formatter:off
    STRING          = 'string'   # string|bytes|enum|fixed
    NUMBER          = 'number'   # float|double
    INTEGER         = 'integer'  # int|long
    OBJECT          = 'object'   # record|map
    ARRAY           = 'array'    # array
    BOOLEAN         = 'boolean'  # bool
    ENUM            = 'enum'     # array or string enumeration
    # @formatter:on

    def empty_value(self) -> Any:
        """TODO"""
        if self.value == 'boolean':
            return False
        elif self.value == 'integer':
            return 0
        elif self.value == 'number':
            return 0.0
        elif self.value == 'object':
            return defaultdict()
        elif self.value == 'array':
            return []
        else:
            return ''

    def is_primitive(self) -> bool:
        return self.value not in ['object', 'array']

    def is_object(self):
        """TODO"""
        return self.value == 'object'
