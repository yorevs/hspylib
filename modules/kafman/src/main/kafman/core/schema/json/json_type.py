#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Kafman
   @package: kafman.core.schema.json.property
      @file: json_type.py
   @created: Wed, 8 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from collections import defaultdict
from hspylib.core.enums.enumeration import Enumeration
from typing import Any


class JsonType(Enumeration):
    """TODO"""

    # fmt: off
    STRING          = 'string'   # string|bytes|enum|fixed
    NUMBER          = 'number'   # float|double
    INTEGER         = 'integer'  # int|long
    OBJECT          = 'object'   # record|map
    ARRAY           = 'array'    # array
    BOOLEAN         = 'boolean'  # bool
    ENUM            = 'enum'     # array or string enumeration
    # fmt: on

    def empty_value(self) -> Any:
        """TODO"""

        if self.value == "boolean":
            value = False
        elif self.value == "integer":
            value = 0
        elif self.value == "number":
            value = 0.0
        elif self.value == "object":
            value = defaultdict()
        elif self.value == "array":
            value = []
        else:
            value = ""

        return value

    def is_primitive(self) -> bool:
        return self.value not in ["object", "array"]

    def is_object(self):
        """TODO"""
        return self.value == "object"
