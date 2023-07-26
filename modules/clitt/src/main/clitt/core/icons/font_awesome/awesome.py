#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core.icons.font_awesome
      @file: awesome.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.commons import sysout
from typing import Union

import re
import struct


class Awesome(Enumeration):
    """
    Font awesome codes
    Full list of font awesome icons can be found here:
      - https://fontawesome.com/cheatsheet?from=io
    """

    @classmethod
    def no_icon(cls) -> "Awesome":
        """No awesome icon specified."""

        def _str(self) -> str:
            return " "

        def _len(self) -> int:
            return 1

        def _fmt(self, fmt) -> str:
            return " "

        no_icon_cls = type("NoIcon", (object,), {"name": "NO_ICON", "value": ""})
        setattr(no_icon_cls, "__str__", _str)
        setattr(no_icon_cls, "__len__", _len)
        setattr(no_icon_cls, "__format__", _fmt)
        return no_icon_cls()

    @staticmethod
    def print_unicode(uni_code: Union[str, int], end: str = "") -> None:
        """Print the specified unicode character.
        :param uni_code: the unicode to be printed.
        :param end string appended after the last value, default a newline.
        """
        if isinstance(uni_code, str) and re.match(r"^[a-fA-F0-9]{1,4}$", uni_code):
            hex_val = bytes.decode(struct.pack("!I", int(uni_code.zfill(4), 16)), "utf_32_be")
            sysout(f"{hex_val:2s}", end=end)
        elif isinstance(uni_code, int):
            hex_val = bytes.decode(struct.pack("!I", uni_code), "utf_32_be")
            sysout(f"{hex_val:2s}", end=end)
        else:
            raise TypeError(f"Invalid unicode value: {uni_code}")

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)

    def __len__(self) -> int:
        return len(str(self.value))

    @property
    def unicode(self) -> str:
        return str(self.value)
