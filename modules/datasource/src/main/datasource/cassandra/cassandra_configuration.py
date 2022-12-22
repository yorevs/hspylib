#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: datasource.cassandra
      @file: cassandra_configuration.py
   @created: Sat, 12 Nov 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Optional

from datasource.db_configuration import DBConfiguration


class CassandraConfiguration(DBConfiguration):
    """Represents a Cassandra datasource configuration"""

    def __init__(self, resource_dir: str, filename: Optional[str] = None, profile: Optional[str] = None):
        super().__init__(resource_dir, filename, profile)
        self._secure_bundle_path = self["datasource.secure_bundle_path"]
        self._protocol_version = self["datasource.protocol_version"] or 4
        self._connect_timeout = self["datasource.connect_timeout"] or 30
        self._default_timeout = self["datasource.default_timeout"] or 60

    @property
    def secure_bundle_path(self) -> str:
        return self._secure_bundle_path

    @property
    def protocol_version(self) -> int:
        return self._protocol_version

    @property
    def connect_timeout(self) -> int:
        return self._connect_timeout

    @property
    def default_timeout(self) -> int:
        return self._default_timeout
