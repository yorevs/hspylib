#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.eventbus
      @file: event.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.namespace import Namespace


class Event:
    """TODO"""

    def __init__(self, event_name: str, **kwargs):
        self._name = event_name
        self._args = Namespace("EventArgs", True, **kwargs)

    def __str__(self) -> str:
        return f"Event(name={self.name})"

    def __repr__(self):
        return str(self)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: "Event") -> bool:
        if isinstance(other, self.__class__):
            return self.name == other.name
        return NotImplemented

    def __getitem__(self, item: str):
        return getattr(self, item)

    @property
    def name(self) -> str:
        return self._name

    @property
    def args(self) -> object:
        return self._args
