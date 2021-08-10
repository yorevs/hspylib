#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: consumer_config.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from abc import ABC


class ConsumerConfig(ABC):  # pylint: disable=too-few-public-methods
    """TODO"""

    BOOTSTRAP_SERVERS = 'bootstrap.servers'
    GROUP_ID = 'group.id'
    CLIENT_ID = 'client.id'
    ENABLE_AUTO_COMMIT = 'enable.auto.commit'
    SESSION_TIMEOUT_MS = 'session.timeout.ms'
    AUTO_OFFSET_RESET = 'auto.offset.reset'
    KEY_DESERIALIZER = 'key.deserializer'
    VALUE_DESERIALIZER = 'value.deserializer'
