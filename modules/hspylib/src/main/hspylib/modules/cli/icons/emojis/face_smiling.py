#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.cli.icons.emojis
      @file: face_smiling.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from enum import auto

from hspylib.modules.cli.icons.emojis.emojis import Emoji


class FaceSmiling(Emoji):
    """
    Face smiling emojis.
    Codes can be found here:
    - https://unicode.org/emoji/charts/emoji-list.html#face-smiling
    """

    # fmt: off
    _CUSTOM         = auto()
    DEFAULT         = '\U0001F600'      # 😀
    BEAMING         = '\U0001F601'      # 😁
    TEARS_OF_JOY    = '\U0001F602'      # 😂
    BIG_EYES        = '\U0001F603'      # 😃
    SMILING_EYES    = '\U0001F604'      # 😄
    SWEAT           = '\U0001F605'      # 😅
    SQUINTING       = '\U0001F606'      # 😆
    HALO            = '\U0001F607'      # 😇
    WINKING         = '\U0001F609'      # 😉
    BLUSHING        = '\U0001F60A'      # 😊
    SLIGHTLY        = '\U0001F642'      # 🙂
    UPSIDE_DOWN     = '\U0001F643'      # 🙃
    ROFL            = '\U0001F923'      # 🤣

    # fmt: on

    @classmethod
    def demo_emojis(cls) -> None:
        list(map(Emoji.emj_print, cls.values()))


if __name__ == "__main__":
    FaceSmiling.demo_emojis()
