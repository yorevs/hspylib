#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib-kafman
   @package: hspylib-kafman.main.kafman.core.schema.field
      @file: map_field.py
   @created: Wed, 1 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HomeSetup team
"""

from typing import Optional

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.field.schema_field_type import AvroType


class MapField(SchemaField):

    def __init__(
        self,
        name: str,
        doc: str,
        values: dict,
        default: str = None,
        required: bool = True):
        super().__init__(
            name,
            doc,
            AvroType.MAP,
            default, required=required)

        self.values = values

    def get_value(self) -> Optional[dict]:
        pass
