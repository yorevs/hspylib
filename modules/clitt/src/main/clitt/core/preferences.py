#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core
      @file: preferences.py
   @created: Fri, 7 Jul 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from enum import Enum
from hspylib.core.metaclass.singleton import AbstractSingleton
from hspylib.core.preconditions import check_argument, check_not_none
from hspylib.core.tools.dict_tools import get_or_default_by_key
from hspylib.core.tools.text_tools import ensure_startswith, environ_name
from typing import Any

import os


class Preferences(metaclass=AbstractSingleton):
    """General purpose bas class to provide preference management."""

    def __init__(self, prefix: str = ""):
        self._prefix = prefix
        self._overrides = {}

    def __str__(self):
        # fmt: off
        return (
            f"Terminal UI Preferences{os.linesep}"
            f"{'-=' * 20}{os.linesep}"
            + os.linesep.join([f"|-{p[1:]:<16}: {getattr(self, p)}" for p in vars(self)])
            + f"{os.linesep}{'-=' * 20}{os.linesep}"
        )
        # fmt: on

    def __repr__(self):
        return str(self)

    def __getitem__(self, name: str):
        attr_name = name.replace(self._prefix + ".", "").replace(".", "_")
        return getattr(self, attr_name)

    def __setitem__(self, name: str, value: Any):
        attr_name = name.replace(self._prefix + ".", "").replace(".", "_")
        curr_val = getattr(self, attr_name)
        t1, t2 = type(curr_val), type(value)
        check_not_none(curr_val, f"Preference '{name}' does not exist")
        check_argument(t1 == t2, f"Preference '{name}' value must be of type '{t1}', not '{t2}'")
        self._overrides[self._get_name(name)] = value

    def __iter__(self):
        return self._overrides.__iter__()

    def __len__(self):
        return len(self._overrides)

    def get_preference(self, name: str, default: Any = None) -> Any:
        """Retrieve preference for the given specified name. If not found, return the default value.
        :param name: the preference name.
        :param default: the preference default value.
        :return the preference value.
        """
        pref_name = self._get_name(name)
        value = get_or_default_by_key(self._overrides, pref_name, default)
        if str_value := os.environ.get(environ_name(pref_name)):
            type_attr = type(value)
            try:
                if isinstance(value, Enum):
                    value = type_attr[str_value.upper()]
                else:
                    value = type_attr(str_value)
            except (KeyError, TypeError, ValueError):
                pass
        return value

    def _get_name(self, name: str) -> str:
        """Retrieve the preference name based. It uses the specified prefix to compose the actual name.
        :param name: the preference name.
        :return the prefixed preference name.
        """
        return ensure_startswith(name, self._prefix + ".")
