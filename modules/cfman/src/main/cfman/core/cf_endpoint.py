#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-CFMan
   @package: cfman.core
      @file: cf_endpoint.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from cfman.exception.exceptions import CFInvalidEndpoint
from hspylib.core.tools.commons import str_to_bool


class CFEndpoint:
    """Represent a cf API endpoint entry."""

    def __init__(self, *attrs: str):
        if len(attrs) != 3:
            raise CFInvalidEndpoint(
                f"Invalid endpoint provided: {str(attrs)}\n" f"Expected format is: <alias,host,protected[true/false]>"
            )
        self._alias = attrs[0]
        self._host = attrs[1]
        self._protected = str_to_bool(attrs[2])

    def __str__(self) -> str:
        return f"{self.alias}  {self.host}"

    def __repr__(self):
        return str(self)

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def host(self) -> str:
        return self._host

    @property
    def protected(self) -> bool:
        return self._protected
