#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.setman
      @file: settings_config.py
   @created: Mon, 5 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from datasource.db_configuration import DBConfiguration
from hspylib.core.config.path_object import PathObject
from hspylib.core.tools.commons import to_bool


class SettingsConfig(DBConfiguration):
    """Holds the settings configurations."""

    INSTANCE = None

    def __init__(self, resource_dir: str, filename: str):
        super().__init__(resource_dir, filename)
        self._database: str = str(PathObject.of(self["hhs.settings.database"]))
        self._encode_db: bool = to_bool(self["hhs.settings.encode.database"])
        SettingsConfig.INSTANCE = self if SettingsConfig.INSTANCE is None else SettingsConfig.INSTANCE

    @property
    def database(self) -> str:
        """Return the settings database name."""
        return self._database

    @property
    def is_db_encoded(self) -> bool:
        """Return the settings encode database."""
        return self._encode_db

    @property
    def encoded_db(self) -> str:
        """Return the settings encoded-database name."""
        return f"{self.database}-encoded"

    @property
    def decoded_db(self) -> str:
        """Return the settings decoded-database name."""
        return f"{self.database}-decoded"
