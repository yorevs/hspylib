#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.cfman.core
      @file: cf_endpoint.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import Tuple


class CFEndpoint:
    """TODO"""

    def __init__(self, attrs: Tuple[str]):
        self.alias = attrs[0]
        self.host = attrs[1]
        self.protected = attrs[2]

    def __str__(self) -> str:
        return f"{self.alias}  {self.host}"

    def __repr__(self):
        return str(self)
