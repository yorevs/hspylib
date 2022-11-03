#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.crud.db
      @file: sqlite_configuration.py
   @created: Thu, 03 Nov 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Optional

from hspylib.core.datasource.db_configuration import DBConfiguration


class SQLiteConfiguration(DBConfiguration):
    """TODO"""

    def __init__(
        self,
        resource_dir: str,
        filename: Optional[str] = None,
        profile: Optional[str] = None):

        super().__init__(resource_dir, filename, profile)
        self._db_file = self['datasource.db.file']

    @property
    def db_file(self) -> str:
        return self._db_file
