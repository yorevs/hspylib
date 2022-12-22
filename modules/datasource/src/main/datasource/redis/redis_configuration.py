#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: datasource.firebase
      @file: firebase_configuration.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Optional

from hspylib.core.config.app_config import AppConfigs


class RedisConfiguration(AppConfigs):
    """Represents a Redis datasource configuration"""

    def __init__(self, resource_dir: str, filename: Optional[str] = None, profile: Optional[str] = None):
        super().__init__(resource_dir, filename, profile)
        self._hostname = self["datasource.hostname"]
        self._database = self["datasource.database"]
        self._port = self["datasource.port"]
        self._username = self["datasource.username"]
        self._password = self["datasource.password"]
        self._ssl = self["datasource.ssl"] or False

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def port(self) -> int:
        return self._port

    @property
    def database(self) -> str:
        return self._database

    @property
    def password(self) -> str:
        return self._password

    @property
    def ssl(self) -> bool:
        return self._ssl
