#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib-kafman
   @package: hspylib-kafman.main.kafman.core.schema.field
      @file: fixed_field.py
   @created: Wed, 1 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from kafman.core.schema.avro.avro_type import AvroType
from kafman.core.schema.schema_field import SchemaField

class FixedField(SchemaField):

    def __init__(
        self,
        name: str,
        doc: str,
        size: int):
        super().__init__(
            name,
            doc,
            AvroType.FIXED,
            default=size)
