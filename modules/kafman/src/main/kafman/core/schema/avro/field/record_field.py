#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib-kafman
   @package: hspylib-kafman.main.kafman.core.schema.field
      @file: record_field.py
   @created: Wed, 1 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from avro.schema import Field
from kafman.core.schema.avro.avro_type import AvroType
from kafman.core.schema.schema_field import SchemaField
from typing import Tuple


class RecordField(SchemaField):
    def __init__(self, name: str, doc: str, fields: Tuple[Field], required: bool = True):
        super().__init__(name, doc, AvroType.RECORD, required=required)

        self.fields = fields
