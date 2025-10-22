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
import os
from textwrap import dedent, indent

from hspylib.modules.cli.keyboard import Keyboard

from clitt.core.term.cursor import cursor
from clitt.core.tui.line_input.keyboard_input import KeyboardInput
from clitt.core.tui.line_input.line_input import line_input


def menu():
    global MENU
    MENU = dedent(f"""
    # Menu
    {os.linesep.join([
        indent(f"{idx}. {entry}", '    ' if idx > 1 else '')
        for idx, entry in enumerate(KeyboardInput.history(), start=1)
    ])}

    `> Who is it ? ` """)


if __name__ == "__main__":
    global MENU
    if os.path.exists('history.txt'):
        KeyboardInput.preload_history_file('history.txt')
    else:
        KeyboardInput.preload_history(["Hugo", "Joao", "Koko", "Hugo", "Koko"])

    menu()

    while (name := line_input(MENU, "Input your name", navbar_enable=True, case_insensitive=False, markdown=True)) \
        not in ["bye", "", None]:
        if isinstance(name, Keyboard):
            cursor.writeln("PTT: " + str(name))
        else:
            cursor.writeln("Input: " + name)
        menu()

    cursor.writeln(KeyboardInput.history())
    KeyboardInput.save_history_file('history.txt')
