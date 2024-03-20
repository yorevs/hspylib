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
    text_color: VtColor = VtColor.NC,
    navbar_enable: bool = False
) -> Optional[str | Keyboard]:
    """Read a string from standard input.
    :param prompt: The message to be displayed to the user.
    :param prompt_color: The color of the prompt text.
    :param text_color: The color of the input text.
    :param navbar_enable: Whether to display the navbar or not.
    """
    ptt = KeyboardInput(prompt, prompt_color, text_color, navbar_enable)
    return ptt.execute()
