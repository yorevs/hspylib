#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.config
      @file: app_config.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import logging as log
import os
import re
from textwrap import dedent
from typing import Any, Optional, TypeAlias

from hspylib.core.config.path_object import PathObject
from hspylib.core.config.properties import Properties
from hspylib.core.metaclass.classpath import AnyPath
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import root_dir, to_bool
from hspylib.core.tools.dict_tools import get_or_default_by_key

Placeholder: TypeAlias = None | dict[str, Any]


class AppConfigs(metaclass=Singleton):
    """Holds all of the application configurations (properties)"""

    INSTANCE = None

    DISPLAY_FORMAT = dedent(
        """
    AppConfigs
      |-Run-dir = {}
      |-Resources-dir = {}
      |-Properties:
       \\-{}
    """
    )

    @staticmethod
    def _replace_holders(value: str, placeholders: Placeholder) -> str:
        """Replace all placeholders by their associated value."""
        replacements = {k.casefold(): v for k, v in placeholders.items()} if placeholders else {}
        re_ph = r'\$\{(\w+)\}'
        pattern = re.compile(re_ph, flags=re.IGNORECASE)
        while match := pattern.search(value):
            key = match.group(1)
            repl = os.environ.get(key, str(get_or_default_by_key(replacements, key, None)))
            re_placeholder = r'\$\{' + re.escape(key) + r'\}'
            value = re.sub(re_placeholder, repl, value, flags=re.IGNORECASE)

        return value

    def __init__(self, resource_dir: AnyPath, filename: str | None = None, profile: str | None = None):
        path_obj = PathObject.of(resource_dir)
        check_argument(path_obj.exists, "Unable to locate resources dir: {}", resource_dir)
        self._resource_dir = str(path_obj)
        self._properties = Properties(filename=filename, load_dir=resource_dir, profile=profile)
        log.info(self)

    # pylint: disable=consider-using-f-string
    def __str__(self) -> str:
        return "\n{}{}{}".format(
            "-=" * 40,
            self.DISPLAY_FORMAT.format(
                str(root_dir()),
                str(self._resource_dir),
                str(self._properties).replace(os.linesep, f"{os.linesep}   |-") if self._properties.size > 0 else "",
            ),
            "-=" * 40,
        )

    def __repr__(self):
        return str(self)

    def __getitem__(self, item: str) -> Optional[str]:
        return self.get(item)

    def __len__(self) -> int:
        return self.size

    @property
    def resource_dir(self) -> Optional[str]:
        """Return the configured application resource dir."""
        return self._resource_dir

    @property
    def properties(self) -> Properties:
        """Return the application properties."""
        return self._properties

    @property
    def size(self) -> int:
        """Return the application properties."""
        return self._properties.size

    def get(self, key: str, placeholders: Placeholder = None) -> Optional[Any]:
        """Get the value, as a string, of a property specified by key, otherwise None is returned.
        :param key: the key name of the property.
        :param placeholders: optional placeholders replacement.
        """
        return self._replace_holders(self._properties.get(key), placeholders)

    def get_int(self, key: str, placeholders: Placeholder = None) -> Optional[int]:
        """Get the value, as an integer, of a property specified by key, otherwise None is returned."""
        return Properties.convert_type(self._replace_holders(self._properties.get(key), placeholders), int)

    def get_float(self, key: str, placeholders: Placeholder = None) -> Optional[float]:
        """Get the value, as a float, of a property specified by key, otherwise None is returned."""
        return Properties.convert_type(self._replace_holders(self._properties.get(key), placeholders), float)

    def get_bool(self, key: str, placeholders: Placeholder = None) -> Optional[bool]:
        """Get the value, as a boolean, of a property specified by key, otherwise None is returned."""
        return Properties.convert_type(self._replace_holders(self._properties.get(key), placeholders), to_bool)
