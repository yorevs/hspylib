#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core.tui
      @file: tui_preferences.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from clitt.core.icons.font_awesome.form_icons import FormIcons
from clitt.core.icons.font_awesome.nav_icons import Awesome, NavIcons
from clitt.core.preferences import Preferences
from hspylib.modules.cli.vt100.vt_color import VtColor


class TUIPreferences(Preferences):
    """Terminal UI Preferences class."""

    INSTANCE = None

    def __init__(self):
        super().__init__("hhs.clitt")

    @property
    def max_rows(self) -> int:
        return max(3, self.get_preference("max.rows", 10))

    @property
    def items_per_line(self) -> int:
        return max(2, self.get_preference("items.per.line", 6))

    @property
    def title_line_length(self) -> int:
        return max(15, self.get_preference("title.line.len", 30))

    @property
    def title_color(self) -> VtColor:
        return self.get_preference("title.color", VtColor.ORANGE)

    @property
    def caption_color(self) -> VtColor:
        return self.get_preference("caption.color", VtColor.WHITE)

    @property
    def text_color(self) -> VtColor:
        return self.get_preference("text.color", VtColor.WHITE)

    @property
    def success_color(self) -> VtColor:
        return self.get_preference("success.color", VtColor.GREEN)

    @property
    def warning_color(self) -> VtColor:
        return self.get_preference("warning.color", VtColor.YELLOW)

    @property
    def error_color(self) -> VtColor:
        return self.get_preference("error.color", VtColor.RED)

    @property
    def highlight_color(self) -> VtColor:
        return self.get_preference("highlight.color", VtColor.CYAN)

    @property
    def navbar_color(self) -> VtColor:
        return self.get_preference("navbar.color", VtColor.YELLOW)

    @property
    def tooltip_color(self) -> VtColor:
        return self.get_preference("tooltip.color", VtColor.GREEN)

    @property
    def breadcrumb_color(self) -> VtColor:
        return self.get_preference("breadcrumb.color", VtColor.compose(VtColor.BG_BLUE, VtColor.WHITE))

    @property
    def sel_bg_color(self) -> VtColor:
        return self.get_preference("sel.bg.color", VtColor.BLUE)

    @property
    def selected_icon(self) -> Awesome:
        return self.get_preference("selected.icon", NavIcons.POINTER)

    @property
    def unselected_icon(self) -> Awesome:
        return self.get_preference("unselected.icon", Awesome.no_icon())

    @property
    def checked_icon(self) -> Awesome:
        return self.get_preference("checked.icon", FormIcons.MARKED)

    @property
    def unchecked_icon(self) -> Awesome:
        return self.get_preference("unchecked.icon", FormIcons.UNMARKED)


assert TUIPreferences().INSTANCE is not None, "Failed to create TUIPreferences instance"
