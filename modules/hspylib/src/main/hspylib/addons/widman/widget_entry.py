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

   Copyright 2022, HSPyLib team
"""
import os

from hspylib.core.tools.text_tools import camelcase


class WidgetEntry:
    """Placeholder object for a HSPyLib::Widman Widget and details about it."""

    # fmt: off
    MODULE_PREFIX   = "widget_"
    CLASS_PREFIX    = "Widget"
    # fmt: on

    def __init__(self, file: str, path: str):
        self._module = os.path.splitext(file)[0]
        self._name = camelcase(self.module.replace(self.MODULE_PREFIX, ""), upper=True)
        self._clazz = f"{self.CLASS_PREFIX}{self.name.replace('_', '')}"
        self._path = path

    def __str__(self):
        return f"{self.name}: {self.module}.{self.clazz} => {self.path}"

    def __repr__(self):
        return str(self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def module(self) -> str:
        return self._module

    @property
    def clazz(self) -> str:
        return self._clazz

    @property
    def path(self) -> str:
        return self._path
