#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.icons.emojis
      @file: emojis.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from emoji.core import emojize

from hspylib.core.enums.enumeration import Enumeration


def emj_print(emoji_str: str) -> None:
    print(emojize(emoji_str) + ' ', end='')


class Emoji(Enumeration):
    """
        Emoji codes
        Full list of emojis can be found here:
          - https://unicode.org/emoji/charts/emoji-list.html
    """

    def __str__(self) -> str:
        return str(self.value)

    def placeholder(self) -> str:
        return f":{self.name}:"
