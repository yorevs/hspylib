#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.icons.emojis.faces
      @file: face_smiling.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.modules.cli.icons.emojis.emojis import emj_print, Emoji


class FaceSmiling(Emoji):
    """
        Face smiling emojis.
        Codes can be found here:
        - https://unicode.org/emoji/charts/emoji-list.html#face-smiling
    """
    DEFAULT = '\U0001F600'
    BEAMING = '\U0001F601'
    TEARS_OF_JOY = '\U0001F602'
    BIG_EYES = '\U0001F603'
    SMILING_EYES = '\U0001F604'
    SWEAT = '\U0001F605'
    SQUINTING = '\U0001F606'
    HALO = '\U0001F607'
    WINKING = '\U0001F609'
    BLUSHING = '\U0001F60A'
    SLIGHTLY = '\U0001F642'
    UPSIDE_DOWN = '\U0001F643'
    ROFL = '\U0001F923'

    @classmethod
    def demo_emojis(cls) -> bool:
        list(map(emj_print, cls.values()))


if __name__ == '__main__':
    FaceSmiling.demo_emojis()
