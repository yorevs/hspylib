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
from textwrap import dedent

from clitt.core.term.cursor import cursor
from clitt.core.tui.line_input.keyboard_input import KeyboardInput
from clitt.core.tui.line_input.line_input import line_input
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.vt_color import VtColor

if __name__ == "__main__":
    MENU = dedent(f"""
    {"-=" * 30}
    1. Hugo
    2. Joao
    3. Koko
    4. Hugo
    5. Koko
    Who is it
    > """)
    hist = ["Hugo", "Joao", "Koko", "Hugo", "Koko"]
    KeyboardInput.preload_history(hist)
    while (name := line_input(MENU, "Input your name", VtColor.YELLOW, VtColor.GREEN, True)) not in ["bye", "", None]:
        if isinstance(name, Keyboard):
            cursor.writeln("PTT: " + name)
        else:
            cursor.writeln("Input: " + name)
    cursor.writeln(KeyboardInput.history())
