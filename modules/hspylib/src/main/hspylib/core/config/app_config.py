#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.core.config
      @file: app_config.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import logging as log
import os
from textwrap import dedent
from typing import Any, Optional

from hspylib.core.config.properties import Properties
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import run_dir, str_to_bool


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

    def __init__(self, resource_dir: str, filename: str | None = None, profile: str | None = None):
        check_argument(os.path.exists(resource_dir), "Unable to locate resources dir: {}", resource_dir)
        self._resource_dir = resource_dir
        self._properties = Properties(filename=filename, load_dir=resource_dir, profile=profile)
        log.info(self)

    # pylint: disable=consider-using-f-string
    def __str__(self) -> str:
        return "\n{}{}{}".format(
            "-=" * 40,
            self.DISPLAY_FORMAT.format(
                str(run_dir()),
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
        """Return the configured application resource dir"""
        return self._resource_dir

    @property
    def properties(self) -> Properties:
        """Return the application properties"""
        return self._properties

    @property
    def size(self) -> int:
        """Return the application properties"""
        return self._properties.size

    def get(self, property_name: str) -> Optional[Any]:
        """Get the value, as a string, of a property specified by property_name, otherwise None is returned"""
        return self._properties.get(property_name)

    def get_int(self, property_name: str) -> Optional[int]:
        """Get the value, as an integer, of a property specified by property_name, otherwise None is returned"""
        return self._properties.get(property_name, cb_to_type=int)

    def get_float(self, property_name: str) -> Optional[float]:
        """Get the value, as a float, of a property specified by property_name, otherwise None is returned"""
        return self._properties.get(property_name, cb_to_type=float)

    def get_bool(self, property_name: str) -> Optional[bool]:
        """Get the value, as a boolean, of a property specified by property_name, otherwise None is returned"""
        return self._properties.get(property_name, cb_to_type=str_to_bool)
