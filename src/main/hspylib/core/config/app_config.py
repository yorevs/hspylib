#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.config
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
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import dirname, environ_name, log_init

APP_CONFIG_FORMAT = """
AppConfigs
  |-SourceDir = {}
  |-ResourceDir = {}
  |-LogFile = {}
  |-AppProperties:
   \\-{}
"""


class AppConfigs(metaclass=Singleton):
    """TODO"""
    
    def __init__(
            self,
            source_root: str = None,
            resource_dir: str = None,
            log_dir: str = None,
            log_file: str = None):
        self._source_dir = source_root \
            if source_root else os.environ.get('SOURCE_ROOT', dirname(__file__))
        assert os.path.exists(self._source_dir), f"Unable to find the source dir: {self._source_dir}"
        
        self._resource_dir = resource_dir \
            if resource_dir else os.environ.get('RESOURCE_DIR', f"{self._source_dir}/resources")
        assert os.path.exists(self._resource_dir), f"Unable to find the resources dir: {self._resource_dir}"
        
        self._log_dir = log_dir \
            if log_dir else os.environ.get('LOG_DIR', f"{self._resource_dir}/log")
        assert os.path.exists(self._log_dir), f"Unable to find the log dir: {self._log_dir}"
        
        self._log_file = log_file \
            if log_file else f"{self._log_dir}/application.log"
        
        assert log_init(self._log_file), f"Unable to create logger: {self._log_file}"
        
        self._app_properties = Properties(load_dir=self._resource_dir)
        log.info(self)
    
    def __str__(self):
        return '\n{}{}{}'.format(
            '-=' * 40,
            APP_CONFIG_FORMAT.format(
                str(self._source_dir),
                str(self._resource_dir),
                str(self._log_file),
                str(self._app_properties).replace('\n', '\n   |-')
                if self._app_properties.size() > 0 else ''
            ),
            '-=' * 40
        )
    
    def __repr__(self):
        return str(self)
    
    def __getitem__(self, item: str) -> Any:
        return self.get(item)
    
    def size(self) -> int:
        return self._app_properties.size()
    
    def source_dir(self) -> Optional[str]:
        return self._source_dir
    
    def resource_dir(self) -> Optional[str]:
        return self._resource_dir
    
    def log_dir(self) -> Optional[str]:
        return self._log_dir
    
    def get(self, property_name: str) -> Optional[str]:
        env_value = os.environ.get(environ_name(property_name))
        return str(env_value) if env_value else self._app_properties.get(property_name)
    
    def get_int(self, property_name: str) -> Optional[int]:
        env = os.environ.get(environ_name(property_name))
        return int(env) if env else self._app_properties.get_int(property_name)
    
    def get_float(self, property_name: str) -> Optional[float]:
        env = os.environ.get(environ_name(property_name))
        return float(env) if env else self._app_properties.get_float(property_name)
    
    def get_bool(self, property_name: str) -> Optional[bool]:
        env = os.environ.get(environ_name(property_name))
        return bool(env) if env else self._app_properties.get_bool(property_name)
