#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib-kafman
   @package: hspylib-kafman.main.kafman.core.schema.json.property
      @file: property_factory.py
   @created: Fri, 1 Jul 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from abc import ABC
from typing import List, Tuple

from hspylib.core.exception.exceptions import InvalidStateError
from hspylib.core.preconditions import check_not_none

from kafman.core.schema.json.json_type import JsonType
from kafman.core.schema.json.property.array_property import ArrayProperty
from kafman.core.schema.json.property.enum_property import EnumProperty
from kafman.core.schema.json.property.object_property import ObjectProperty
from kafman.core.schema.json.property.primitive_property import PrimitiveProperty
from kafman.core.schema.json.property.property import Property
from kafman.core.schema.schema_field import SchemaField


class PropertyFactory(ABC):
    @staticmethod
    def create_field(p_property: Property) -> "SchemaField":
        """TODO"""

        check_not_none(p_property)
        prop_name, prop_type = p_property.name, p_property.type
        prop_doc = p_property.description or f"the {prop_name}"
        prop_default = p_property.default
        required = p_property.required
        prop_type = p_property.type

        if p_property.type.is_primitive():
            schema_field = PrimitiveProperty(prop_name, prop_doc, prop_type, prop_default, required)
        elif p_property.type == JsonType.ARRAY:
            if hasattr(p_property.extras, "a_items"):
                schema_field = ArrayProperty(prop_name, prop_doc, p_property.extras.a_items, required)
            elif hasattr(p_property.extras, "enum"):
                schema_field = EnumProperty(prop_name, prop_doc, p_property.extras.enum, prop_default, required)
            else:
                schema_field = ArrayProperty(prop_name, prop_doc, [], required)
        elif p_property.type == JsonType.OBJECT:
            properties = p_property.all_properties
            schema_field = ObjectProperty(prop_name, prop_doc, tuple(properties), required)
        else:
            raise InvalidStateError(f"Invalid field type: {p_property.type}")

        check_not_none(schema_field, f"Unable to parse field {prop_name}")

        return schema_field

    @staticmethod
    def create_schema_fields(fields: Tuple[Property]) -> List[SchemaField]:
        """TODO"""
        record_fields = []
        for next_field in fields:
            field = PropertyFactory.create_field(next_field)
            record_fields.append(field)

        return record_fields
