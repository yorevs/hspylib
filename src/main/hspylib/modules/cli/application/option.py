#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.application
      @file: option.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Callable


class Option:
    
    def __init__(
            self,
            shortopt: chr,
            longopt: str,
            has_argument: bool = False,
            cb_handler: Callable = None):
        self.name = longopt.replace('--', '')
        self.shortopt = f"-{shortopt.replace('-', '')}{':' if has_argument > 0 else ''}"
        self.longopt = f"--{longopt.replace('--', '')}{'=' if has_argument > 0 else ''}"
        self.has_argument = has_argument
        self.cb_handler = cb_handler
    
    def __str__(self) -> str:
        return ("name: {}, shortopt: {}, longopt: {}, has_argument: {}, cb_handler: {}".format(
            self.name, self.shortopt, self.longopt, self.has_argument, self.cb_handler))
    
    def __repr__(self):
        return f"[{self.shortopt.replace('-', '').replace(':', '')}, {self.longopt.replace('--', '').replace('=', '')}]"

    def is_eq(self, other: str) -> bool:
        clean_opt = other.replace('-', '').replace(':', '').replace('=', '').strip()
        return \
            clean_opt == self.shortopt.replace('-', '').replace(':', '').strip() or \
            clean_opt == self.longopt.replace('--', '').replace('=', '').strip()
