#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: producer_config.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from abc import ABC


class ProducerConfig(ABC):
    """TODO"""

    BOOTSTRAP_SERVERS = 'bootstrap.servers'
    KEY_SERIALIZER = 'key.serializer'
    VALUE_SERIALIZER = 'value.serializer'
    SCHEMA_REGISTRY_URL = 'schema.registry.url'
