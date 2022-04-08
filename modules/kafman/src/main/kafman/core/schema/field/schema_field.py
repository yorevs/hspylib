#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: schema_field.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from abc import ABC, abstractmethod
from typing import Any, Optional

from kafman.core.schema.schema_field_type import SchemaFieldType


class SchemaField(ABC):
    """Represents a schema registry field and form component.
        - Avro Types: https://avro.apache.org/docs/current/spec.html#schema_record
        - Json Types: https://json-schema.org/understanding-json-schema/reference/type.html
    """

    def __init__(
        self,
        name: str,
        doc: str,
        a_type: SchemaFieldType,
        default: Any = None,
        required: bool = True):

        self.name = name
        self.doc = doc
        self.a_type = a_type
        self.default = default
        self.required = required
        self.widget = None

    def __str__(self):
        return \
            f"name={self.name}, " \
            f"type={str(self.a_type)}, " \
            f"required={self.required}, "

    def is_valid(self) -> bool:
        """Whether the field is valid, based on it's values and required flag"""
        return not self.required or self.get_value() is not None

    @abstractmethod
    def get_value(self) -> Optional[dict]:
        """Return the value contained by the schema widget. This may vary depending on the QWidget class"""

    @abstractmethod
    def create_input_widget(self):
        """Return the QWidget type required by this field"""
