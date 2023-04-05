#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.cli.tui
      @file: tui_component.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_tools import elide_text, ensure_endswith
from hspylib.modules.cli.keyboard import Keyboard

from clitt.core.icons.font_awesome.awesome import Awesome
from clitt.core.tui.tui_preferences import TUIPreferences

T = TypeVar("T")


class TUIComponent(Generic[T], ABC):
    """Provide a base class for terminal UI components.
    """

    @staticmethod
    def _draw_line(line_fmt: str, max_columns: int, *args: Any) -> None:
        """TODO
        :param line_fmt: the line format.
        :param max_columns: the maximum length of the line. If the text is greater than this limit, it will be elided.
        :param args: the arguments for the format.
        """
        sysout(ensure_endswith(elide_text(line_fmt.format(*args), max_columns), "%NC%"))

    def __init__(self, title: str = None):
        self.prefs: TUIPreferences = TUIPreferences.INSTANCE or TUIPreferences()
        self._done: bool = False
        self._re_render: bool = True
        self._title: str = title

    @property
    def title(self) -> str:
        return self._title

    @abstractmethod
    def execute(self) -> Optional[T | List[T]]:
        """Execute the main component flow.
        """

    def _draw_line_color(self, is_selected: bool = False, has_bg_color: bool = True) -> Awesome:
        """TODO
        :param is_selected: whether to set a selected foreground color or not.
        :param has_bg_color: whether to set a background or not.
        """
        if is_selected:
            selector = self.prefs.selected
            if has_bg_color:
                sysout(self.prefs.sel_bg_color.code, end="")
            sysout(self.prefs.highlight_color.code, end="")
        else:
            selector = self.prefs.unselected
            sysout(self.prefs.text_color.code, end="")

        return selector

    @abstractmethod
    def _render(self) -> None:
        """Method to render the component.
        """

    @abstractmethod
    def _navbar(self, **kwargs) -> str:
        """Provide the component navigation bar (if applies).
        """

    @abstractmethod
    def _handle_keypress(self) -> Keyboard:
        """Handle a keyboard press.
        """
