#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Kafman
   @package: kafman.views
      @file: indexes.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from hspylib.core.enums.enumeration import Enumeration


class Tabs(Enumeration):
    """TabWidget indexes"""

    PRODUCER = 0
    CONSUMER = 1
    REGISTRY = 2
    CONSOLE = 3


class StkTools(Enumeration):
    """StackedPane Widget 'Tools' indexes"""

    SETTINGS = 0
    SCHEMAS = 1
    STATISTICS = 2


class StkProducerEdit(Enumeration):
    """StackedPane Widget 'ProducerEdit' indexes"""

    TEXT = 0
    FORM = 1
