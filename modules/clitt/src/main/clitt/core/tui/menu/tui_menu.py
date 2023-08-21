#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.menu
      @file: tui_menu.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from abc import ABC
from clitt.core.icons.font_awesome.nav_icons import NavIcons
from clitt.core.tui.minput.input_validator import InputValidator
from clitt.core.tui.minput.menu_input import MenuInput
from clitt.core.tui.minput.minput import minput
from clitt.core.tui.tui_component import TUIComponent
from hspylib.core.namespace import Namespace
from hspylib.modules.cli.keyboard import Keyboard
from typing import Callable, Optional, TypeAlias

OnTrigger_Cb: TypeAlias = Callable[["TUIMenu"], Optional["TUIMenu"]]


class TUIMenu(TUIComponent, ABC):
    """Provide a base class for terminal UI menus."""

    @staticmethod
    def prompt(
        label: str, dest: str = None, min_length: int = 1, max_length: int = 32, validator: InputValidator = None
    ) -> Optional[Namespace]:
        # fmt: off
        form_fields = (
            MenuInput.builder()
                .field()
                .label(label)
                .dest(dest or label)
                .validator(validator or InputValidator.words())
                .min_max_length(min_length, max_length)
                .build()
            .build()
        )
        # fmt: on

        return minput(form_fields)

    def __init__(
        self,
        parent: Optional["TUIMenu"] = None,
        title: str = "",
        tooltip: str = "",
        default_on_trigger_cb: OnTrigger_Cb = None,
    ):
        super().__init__(title)
        self._tooltip = tooltip
        self._parent = parent
        self._on_trigger = default_on_trigger_cb or self._default_trigger_cb

    def __str__(self) -> str:
        return self._title

    def __repr__(self) -> str:
        return str(self)

    @property
    def parent(self) -> Optional["TUIMenu"]:
        return self._parent

    @property
    def tooltip(self) -> str:
        return self._tooltip

    def handle_keypress(self) -> Keyboard:
        if keypress := Keyboard.wait_keystroke():
            match keypress:
                case Keyboard.VK_ENTER | Keyboard.VK_ESC:
                    self._done = True

        return keypress

    def navbar(self, **kwargs) -> str:
        return (
            f"%EOL%{self.breadcrumb()}%ED0%"
            f"%EOL%{self.prefs.navbar_color.placeholder}%EOL%"
            f"[Enter] Back  [Esc] Quit  %EL0%%EOL%%EOL%%NC%"
        )

    def breadcrumb(self) -> str:
        """Provide a breadcrumb of menus for navigation purposes."""
        return (
            f"{self.prefs.breadcrumb_color.placeholder}"
            f" {NavIcons.BREADCRUMB} {self.title} %NC%"
            f"{self.prefs.tooltip_color.placeholder}"
        )

    def wait_keystroke(self, wait_message: str = "%YELLOW%%EOL%Press any key to continue%EOL%%NC%") -> None:
        """Wait for a keypress (blocking).
        :param wait_message: the message to present to the user.
        """
        self.writeln(wait_message)
        Keyboard.wait_keystroke()

    def _default_trigger_cb(self, source: Optional["TUIMenu"]) -> Optional["TUIMenu"]:
        """Provide a default trigger callback when a menu is activated. Provided a source menu, returns it's parent.
        :param source: the source which invoked this menu.
        """
        return self.parent
