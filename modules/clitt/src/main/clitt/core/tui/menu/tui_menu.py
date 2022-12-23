#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: clitt.core.tui.menu
      @file: tui_menu.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, TypeVar

from clitt.core.icons.font_awesome.nav_icons import NavIcons
from clitt.core.keyboard import Keyboard
from clitt.core.tui.tui_component import TUIComponent

ON_TRIGGER_CB = TypeVar('ON_TRIGGER_CB', bound=Callable[['TUIMenu'], Optional['TUIMenu']])


class TUIMenu(TUIComponent, ABC):
    """TODO"""

    def __init__(
        self,
        parent: Optional['TUIMenu'] = None,
        title: Optional[str] = None,
        tooltip: Optional[str] = None):
        super().__init__(title or '')

        self._tooltip: str = tooltip or ''
        self._parent: Optional['TUIMenu'] = parent
        self._on_trigger: ON_TRIGGER_CB = self._default_trigger_cb

    def __str__(self) -> str:
        return self._title

    def __repr__(self) -> str:
        return str(self)

    @property
    def parent(self) -> Optional['TUIMenu']:
        return self._parent

    @property
    def tooltip(self) -> str:
        return self._tooltip

    @abstractmethod
    def execute(self) -> Optional[Any]:
        """TODO"""

    def _handle_keypress(self) -> Keyboard:
        """TODO"""
        if keypress := Keyboard.wait_keystroke():
            match keypress:
                case Keyboard.VK_ENTER | Keyboard.VK_ESC:
                    self._done = True

        return keypress

    def _navbar(self, **kwargs) -> str:
        return (
            f"%EOL%{self._breadcrumb()}%ED0%%NC%"
            f"%EOL%{self.prefs.navbar_color.placeholder}%EOL%"
            f"[Enter] Back  [Esc] Quit  %NC%%EL0%%EOL%%EOL%"
        )

    def _breadcrumb(self) -> str:
        """TODO"""
        return (
            f"{self.prefs.breadcrumb_color.placeholder}"
            f" {NavIcons.BREADCRUMB} {self._title} %NC%"
            f"{self.prefs.tooltip_color.placeholder}"
        )

    def _default_trigger_cb(self, source: Optional['TUIMenu']) -> Optional['TUIMenu']:
        """TODO"""
        return self._parent
