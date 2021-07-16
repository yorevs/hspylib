#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.cfman.src.main.core
      @file: cf_application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import re
from typing import List

from hspylib.core.tools.commons import sysout
from hspylib.core.tools.preconditions import check_argument


class CFApplication:
    max_name_length = 0

    @classmethod
    def of(cls, app_line: str):
        """TODO"""
        parts = re.split(r' {2,}', app_line)
        check_argument(len(parts) >= 6, f"Invalid application line: {app_line}")
        return CFApplication(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5].split(', '))

    def __init__(
            self,
            name: str,
            state: str,
            instances: str,
            memory: str,
            disk: str,
            urls: List[str]):
        self.name = name
        self.state = state
        self.instances = instances
        self.memory = memory
        self.disk = disk
        self.urls = urls
        self.max_name_length = max(self.max_name_length, len(self.name))

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def print_status(self):
        """TODO"""
        sysout("%CYAN%{}  %{}%{:5}  %WHITE%{:5}  {:4}  {:4}  {}".format(
            self.name.ljust(self.max_name_length),
            'GREEN' if self.state == 'started' else 'RED',
            self.state,
            self.instances,
            self.memory,
            self.disk,
            self.urls
        ))
