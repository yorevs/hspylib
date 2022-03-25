#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: producer_config.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from abc import ABC


class ProducerConfig(ABC):  # pylint: disable=too-few-public-methods
    """Some of the confluence exposed producer properties"""

    BOOTSTRAP_SERVERS = 'bootstrap.servers'
    KEY_SERIALIZER = 'key.serializer'
    VALUE_SERIALIZER = 'value.serializer'
    SCHEMA_REGISTRY_URL = 'schema.registry.url'
