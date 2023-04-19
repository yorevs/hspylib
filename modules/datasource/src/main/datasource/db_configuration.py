#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: datasource
      @file: db_configuration.py
   @created: Thu, 03 Nov 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from hspylib.core.config.app_config import AppConfigs
from typing import Optional


class DBConfiguration(AppConfigs):
    """Holds database configurations."""

    def __init__(self, resource_dir: str, filename: str | None = None, profile: str | None = None):
        super().__init__(resource_dir, filename, profile)
        self._hostname = self["datasource.hostname"]
        self._port = self.get_int("datasource.port")
        self._username = self["datasource.username"]
        self._password = self["datasource.password"]
        self._database = self["datasource.database"]

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def port(self) -> int:
        return self._port

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def database(self) -> Optional[str]:
        return self._database
