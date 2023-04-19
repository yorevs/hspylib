#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Kafman
   @package: kafman.core.producer
      @file: producer_config.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from abc import ABC
from typing import List


class ProducerConfig(ABC):
    """Some of the confluence exposed producer properties"""

    BOOTSTRAP_SERVERS = "bootstrap.servers"
    KEY_SERIALIZER = "key.serializer"
    VALUE_SERIALIZER = "value.serializer"

    @classmethod
    def required_settings(cls) -> List[str]:
        return [cls.BOOTSTRAP_SERVERS]

    @classmethod
    def defaults(cls) -> dict:
        return {"producer": {ProducerConfig.BOOTSTRAP_SERVERS: "localhost:9092"}}
