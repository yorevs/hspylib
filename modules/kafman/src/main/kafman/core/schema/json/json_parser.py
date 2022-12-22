#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Kafman
   @package: kafman.core.schema.json
      @file: json_parser.py
   @created: Fri, 1 Jul 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from abc import ABC
from typing import List, Tuple

from hspylib.core.preconditions import check_and_get
from jsonschema.validators import Draft202012Validator

from kafman.core.schema.json.json_type import JsonType
from kafman.core.schema.json.property.property import Property


class JsonParser(ABC):
    """TODO"""

    class JsonSchemaData:  # pylint: disable=too-few-public-methods
        """TODO"""

        def __init__(self):
            self.id = None
            self.schema = None
            self.title = None
            self.description = None
            self.properties = None
            self.required = None
            self.type = None

    @staticmethod
    def parse(schema_dict: dict) -> "JsonSchemaData":
        """TODO"""
        Draft202012Validator(schema=schema_dict, format_checker=None)
        schema = JsonParser.JsonSchemaData()
        schema.id = check_and_get("$id", schema_dict)
        schema.schema = check_and_get("$schema", schema_dict)
        schema.title = check_and_get("title", schema_dict)
        schema.description = check_and_get("description", schema_dict, False)
        schema.required = check_and_get("required", schema_dict, False, [])
        schema.type = check_and_get("type", schema_dict)

        if JsonType.OBJECT.value == schema.type:
            properties = check_and_get("properties", schema_dict, default={})
            schema.properties = JsonParser._parse_properties(properties, schema.required)

        return schema

    @staticmethod
    def _parse_properties(properties: dict, required: List[str]) -> Tuple[Property]:
        """TODO"""

        schema_properties = []
        for p_name, props in properties.items():
            p_title = check_and_get("title", props, False, "")
            p_description = check_and_get("description", props, False, "")
            p_type = JsonType.of_value(check_and_get("type", props))
            p_default = check_and_get("default", props, False)
            p_required = p_name in required

            p_properties = (
                JsonParser._parse_properties(check_and_get("properties", props), required)
                if p_type == JsonType.OBJECT
                else None
            )
            p_items = check_and_get("items", props, False) if p_type == JsonType.ARRAY else None

            prop = Property(p_name, p_title, p_description, p_type, p_default, p_required)
            prop.all_properties = p_properties
            if p_items:
                prop.set_items(p_items)

            schema_properties.append(prop)

        return tuple(schema_properties)
