#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.setman
      @file: setman_config.py
   @created: Mon, 5 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from datasource.db_configuration import DBConfiguration


class SetmanConfig(DBConfiguration):
    """Holds the SetMan configurations."""

    INSTANCE = None

    def __init__(self, resource_dir: str, filename: str):
        super().__init__(resource_dir, filename)
        self._database = self["hhs.setman.database"]

    @property
    def database(self) -> str:
        """Return the SetMan database name."""
        return self._database

    @property
    def encoded_db(self) -> str:
        """Return the SetMan encoded database name."""
        return f"{self.database}-encoded"

    @property
    def decoded_db(self) -> str:
        """Return the SetMan decoded database name."""
        return f"{self.database}-decoded"
