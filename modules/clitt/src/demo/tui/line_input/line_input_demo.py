#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.cli.tui.line_input
      @file: line_input_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from clitt.core.tui.line_input.keyboard_input import KeyboardInput
from clitt.core.tui.line_input.line_input import line_input
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.vt_color import VtColor

if __name__ == "__main__":
    hist = ["Hugo", "Joao", "Koko", "Hugo", "Koko"]
    KeyboardInput.preload_history(hist)
    print("-=" * 30)
    while (i := line_input("What is it? ", "Input your name", VtColor.YELLOW, VtColor.GREEN, True)) not in ["bye", "", None]:
        if isinstance(i, Keyboard):
            print("PTT", i)
        else:
            print("Input:", i)
    print(KeyboardInput.history())
