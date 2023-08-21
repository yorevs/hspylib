#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.menu
      @file: tui_menu_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.term.commons import Direction
from clitt.core.tui.menu.tui_menu import OnTrigger_Cb, TUIMenu
from clitt.core.tui.menu.tui_menu_ui import TUIMenuUi
from typing import Callable, Optional


class TUIMenuView(TUIMenu):
    """Represent a menu view without submenus. Each view can have a view to be displayed. If no view is provided, it
    will behave like an action.
    """

    def __init__(
        self,
        parent: TUIMenu,
        title: Optional[str] = None,
        tooltip: Optional[str] = None,
        display_text: Optional[str] = None,
    ):
        super().__init__(parent, title or "Menu View", tooltip or f"Access the '{title}' view")
        self._on_render: OnTrigger_Cb = self._display_content
        self._content: str = display_text or f"%ED0%This is a view: {self.title}"

    def on_render(self, on_render: str | OnTrigger_Cb) -> None:
        if isinstance(on_render, str):
            self._content = on_render
            self._on_render = self._display_content
        elif isinstance(on_render, Callable):
            self._on_render = on_render
            self._content = f"This is a view: {self.title}"

    def execute(self) -> Optional[TUIMenu]:
        self.render()
        return self._on_trigger(self)

    def render(self) -> None:
        TUIMenuUi.render_app_title()
        self._on_render()
        self.draw_navbar(self.navbar())

    def _display_content(self) -> None:
        self.cursor.erase(Direction.DOWN)
        self.writeln(self._content)
        self.wait_keystroke()
