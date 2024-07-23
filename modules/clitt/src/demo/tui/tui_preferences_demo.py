#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.cli.tui
      @file: tui_preferences_demo.py
   @created: Fri, 7 Jul 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from clitt.core.tui.tui_preferences import TUIPreferences
from hspylib.core.tools.commons import sysout

import os

if __name__ == "__main__":
    prefs = TUIPreferences.INSTANCE
    sysout("max.rows: ", prefs.max_rows)
    sysout("items.per.line: ", prefs.items_per_line)
    sysout("title.line.length: ", prefs.title_line_length, "%NC%")
    sysout("title.color: ", prefs.title_color, prefs.title_color.name, "%NC%")
    sysout("text.color: ", prefs.text_color, prefs.text_color.name, "%NC%")
    sysout("success.color: ", prefs.success_color, prefs.success_color.name, "%NC%")
    sysout("warning.color: ", prefs.warning_color, prefs.warning_color.name, "%NC%")
    sysout("error.color: ", prefs.error_color, prefs.error_color.name, "%NC%")
    sysout("highlight.color: ", prefs.highlight_color, prefs.highlight_color.name, "%NC%")
    sysout("navbar.color: ", prefs.navbar_color, prefs.navbar_color.name, "%NC%")
    sysout("tooltip.color: ", prefs.tooltip_color, prefs.tooltip_color.name, "%NC%")
    sysout("breadcrumb.color: ", prefs.breadcrumb_color, prefs.breadcrumb_color.name, "%NC%")
    sysout("sel_bg.color: ", prefs.sel_bg_color, prefs.sel_bg_color.name, "%NC%")
    sysout("selected.icon: ", prefs.selected_icon, " " + prefs.selected_icon.name, "%NC%")
    sysout("unselected.icon: ", prefs.unselected_icon, " " + prefs.unselected_icon.name, "%NC%")
    sysout("checked.icon: ", prefs.checked_icon, " " + prefs.checked_icon.name, "%NC%")
    sysout("unchecked.icon: ", prefs.unchecked_icon, " " + prefs.unchecked_icon.name, "%NC%")

    prefs["max.rows"] = 20
    sysout("NEW: max.rows: ", prefs["max.rows"])
    sysout("FULL: max.rows: ", prefs["hhs.clitt.max.rows"])

    for p in prefs:
        sysout("Override: ", p, " -> ", prefs[p])

    sysout(prefs, "Length: ", len(prefs))

    os.environ["HHS_CLITT_MAX_ROWS"] = "30"
    os.environ["HHS_CLITT_TEXT_COLOR"] = "VIOLET"
    os.environ["HHS_CLITT_CHECKED_ICON"] = "ATTACH"
    os.environ["HHS_CLITT_SUCCESS_COLOR"] = "NO_EXIST"

    mr = prefs["max.rows"]
    tc = prefs["text.color"]
    ic = prefs["checked.icon"]
    sc = prefs["success.color"]

    sysout("ENV: HHS_CLITT_MAX_ROWS: ", mr, " ", type(mr))
    sysout("ENV: HHS_CLITT_TEXT_COLOR: ", tc, type(tc), "%NC%")
    sysout("ENV: HHS_CLITT_CHECKED_ICON: ", ic, " ", type(ic))
    sysout("ENV: HHS_CLITT_SUCCESS_COLOR: ", sc, " ", type(sc))
