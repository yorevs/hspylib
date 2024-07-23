#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.icons.emojis
      @file: demo_emojis.py
   @created: Tue, 13 Jan 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from clitt.core.icons.emojis.emojis import Emoji
from clitt.core.icons.emojis.face_smiling import FaceSmiling

if __name__ == "__main__":
    print("\nFace Smiling " + "-" * 30)
    list(map(Emoji.emj_print, FaceSmiling.values()))
