#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.cli.tui.menu
      @file: tui_menu_utils.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.namespace import Namespace
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.tui.menu.tui_menu_ui import TUIMenuUi
from hspylib.modules.cli.tui.minput.input_validator import InputValidator
from hspylib.modules.cli.tui.minput.minput import MenuInput, minput


class TUIMenuUtils:

    @staticmethod
    def wait_keystroke(wait_message: str = "%YELLOW%%EOL%Press any key to continue%EOL%%NC%") -> None:
        sysout(wait_message)
        Keyboard.wait_keystroke()

    @classmethod
    def prompt(
        cls,
        label: str,
        dest: str = None,
        min_length: int = 1,
        max_length: int = 32,
        validator: InputValidator = None) -> Namespace:
        form_fields = MenuInput.builder() \
            .field() \
            .label(label) \
            .dest(dest or label) \
            .validator(validator or InputValidator.words(min_length, max_length)) \
            .min_max_length(min_length, max_length) \
            .build() \
            .build()
        ret_val = minput(form_fields)
        TUIMenuUi.render_app_title()
        return ret_val
