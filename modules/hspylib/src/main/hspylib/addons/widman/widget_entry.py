#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   main.addons.widman
      @file: widget_entry.py
   @created: Fri, 04 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import os

from hspylib.core.tools.text_tools import camelcase


class WidgetEntry:
    """Placeholder entry for a HSPyLib Widget and details about it"""

    WIDGET_MODULE_PREFIX = 'widget_'
    WIDGET_CLASS_PREFIX = 'Widget'

    def __init__(self, file: str, path: str):
        self.module = os.path.splitext(file)[0]
        self.name = camelcase(self.module.replace(self.WIDGET_MODULE_PREFIX, ''))
        self.clazz = f"{self.WIDGET_CLASS_PREFIX}{self.name.replace('_', '')}"
        self.path = path

    def __str__(self):
        return f"{self.name}: {self.module}.{self.clazz} => {self.path}"

    def __repr__(self):
        return str(self)
