#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Kafman
   @package: kafman.core.schema.json.property
      @file: property.py
   @created: Fri, 1 Jul 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import Any, List, Union

from hspylib.core.exception.exceptions import InvalidArgumentError
from hspylib.core.namespace import Namespace
from hspylib.core.preconditions import check_and_get

from kafman.core.schema.json.json_type import JsonType


class Property:
    """TODO"""

    def __init__(
        self, name: str, title: str, description: str, s_type: JsonType, default: Any = None, required: bool = True
    ):

        self.name = name
        self.title = title
        self.description = description
        self.type = s_type
        self.default = default
        self.required = required
        self.all_properties = None
        self.extras = Namespace("SchemaAttributes")

    def set_items(self, p_items: Union[List[str], dict]) -> None:
        """TODO"""
        if isinstance(p_items, list):
            self.extras.a_items = p_items
        elif isinstance(p_items, dict):
            self.extras.enum = check_and_get("enum", p_items, False, [])
        else:
            raise InvalidArgumentError(f'Invalid property "items" type: {type(p_items)}')
