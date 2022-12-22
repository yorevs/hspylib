#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Kafman
   @package: kafman.core.schema.avro.field
      @file: primitive_field.py
   @created: Wed, 1 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import Any

from kafman.core.schema.avro.avro_type import AvroType
from kafman.core.schema.schema_field import SchemaField


class PrimitiveField(SchemaField):
    def __init__(self, name: str, doc: str, p_type: AvroType, default: Any = None, required: bool = True):
        super().__init__(name, doc, p_type, default, required=required)
