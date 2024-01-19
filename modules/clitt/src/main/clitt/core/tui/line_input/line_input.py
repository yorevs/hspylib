#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: main.clitt.core.tui.line_input
      @file: line_input.py
   @created: Wed, 17 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.vt_color import VtColor
from typing import Optional

from clitt.core.tui.line_input.keyboard_input import KeyboardInput


def line_input(
    prompt: str = "",
    prompt_color: VtColor = VtColor.NC,
) -> Optional[str | Keyboard]:
    """Read a string from standard input.
    :param prompt: The message to be displayed to the user.
    :param prompt_color: The color of the prompt text.
    """
    ptt = KeyboardInput(prompt, prompt_color)
    return ptt.execute()


if __name__ == "__main__":
    hist = ["Hugo", "Joao", "Koko", "Hugo"]
    KeyboardInput.preload_history(hist)
    print("-=" * 30)
    while (i := line_input("What is it? ")) not in ["bye", ""]:
        if isinstance(i, Keyboard):
            print(i)
        else:
            print("Input:", i)
    print(KeyboardInput.history())
