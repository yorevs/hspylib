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


class Event:
    """TODO"""

    def __init__(self, _name_: str, **kwargs):
        self.name = _name_
        self.kwargs = kwargs

    def __str__(self):
        return f"{self.name}: {str(self.kwargs)}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other: 'Event'):
        return self.name == other.name and self.kwargs == other.kwargs

    def __getitem__(self, item: str):
        return self.kwargs[item]
