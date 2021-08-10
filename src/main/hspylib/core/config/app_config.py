#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: hspylib.main.hspylib.core.config
      @file: app_config.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import os
from typing import Any, Optional

from hspylib.core.config.properties import Properties
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import dirname, log_init
from hspylib.core.tools.preconditions import check_argument, check_state


class AppConfigs(metaclass=Singleton):
    """Holds all of the application configurations (properties)"""

    DISPLAY_FORMAT = """
AppConfigs
  |-SourceDir = {}
  |-ResourceDir = {}
  |-LogFile = {}
  |-AppProperties:
   \\-{}
"""

    def __init__(
        self,
        source_root: str = None,
        resource_dir: str = None,
        log_dir: str = None,
        log_file: str = None):
        self._source_dir = source_root \
            if source_root else os.environ.get('SOURCE_ROOT', dirname(__file__))
        check_argument(os.path.exists(self._source_dir), "Unable to find the source dir: {}", self._source_dir)

        self._resource_dir = resource_dir \
            if resource_dir else os.environ.get('RESOURCE_DIR', f"{self._source_dir}/resources")
        check_argument(os.path.exists(self._resource_dir), "Unable to find the resources dir: {}", self._resource_dir)

        self._log_dir = log_dir \
            if log_dir else os.environ.get('LOG_DIR', f"{self._resource_dir}/log")
        check_argument(os.path.exists(self._log_dir), "Unable to find the log dir: {}", self._log_dir)

        self._log_file = log_file \
            if log_file else f"{self._log_dir}/application.log"
        check_state(log_init(self._log_file), "Unable to create logger: {}", self._log_file)

        self._app_properties = Properties(load_dir=self._resource_dir)
        log.info(self)

    def __str__(self):
        return '\n{}{}{}'.format(
            '-=' * 40,
            self.DISPLAY_FORMAT.format(
                str(self._source_dir),
                str(self._resource_dir),
                str(self._log_file),
                str(self._app_properties).replace('\n', '\n   |-')
                if len(self._app_properties) > 0 else ''
            ),
            '-=' * 40
        )

    def __repr__(self):
        return str(self)

    def __getitem__(self, item: str) -> Any:
        return self.get(item)

    def __len__(self) -> int:
        return len(self._app_properties)

    def source_dir(self) -> Optional[str]:
        """TODO"""
        return self._source_dir

    def resource_dir(self) -> Optional[str]:
        """TODO"""
        return self._resource_dir

    def log_dir(self) -> Optional[str]:
        """TODO"""
        return self._log_dir

    def get(self, property_name: str) -> Optional[str]:
        """TODO"""
        env_value = os.environ.get(Properties.environ_name(property_name))
        return str(env_value) if env_value else self._app_properties.get(property_name)

    def get_int(self, property_name: str) -> Optional[int]:
        """TODO"""
        env = os.environ.get(Properties.environ_name(property_name))
        return int(env) if env else self._app_properties.get_int(property_name)

    def get_float(self, property_name: str) -> Optional[float]:
        """TODO"""
        env = os.environ.get(Properties.environ_name(property_name))
        return float(env) if env else self._app_properties.get_float(property_name)

    def get_bool(self, property_name: str) -> Optional[bool]:
        """TODO"""
        env = os.environ.get(Properties.environ_name(property_name))
        return bool(env) if env else self._app_properties.get_bool(property_name)
