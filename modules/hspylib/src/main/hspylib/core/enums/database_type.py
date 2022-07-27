#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.enum
      @file: database_type.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration


class DatabaseType(Enumeration):
    """TODO"""

    # @formatter:off
    FILE_STORAGE    = 'file-storage'
    MYSQL           = 'mysql'
    POSTGRES_SQL    = 'postgres'
    MONGO_DB        = 'mongo-db'
    # @formatter:on
