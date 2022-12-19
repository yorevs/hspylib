#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.cli.tui
      @file: dynamic_menu_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.modules.cli.tui.menu.tui_menu_factory import TUIMenuFactory
from hspylib.modules.cli.tui.menu.tui_menu_ui import TUIMenuUi

if __name__ == "__main__":
    # fmt: off
    main_menu = TUIMenuFactory \
        .create_main_menu('Dynamic Main Menu', tooltip='Test Dynamic Menus') \
            .with_item('Sub-Menu-1') \
                .with_action("DO IT 1", "Let's do it")\
                    .on_trigger(lambda x: print("ACTION 1")) \
                .with_view("Just a View 1", "Show the view 1")\
                    .on_render("MY BEAUTIFUL VIEW 1") \
                .with_action("Back", "Back to the previous menu")\
                    .on_trigger(lambda x: x.parent) \
                .then() \
            .with_item('Sub-Menu-2') \
                .with_action("DO IT 2", "Let's do it too")\
                    .on_trigger(lambda x: print("ACTION 2")) \
                .with_view("Just a View 2", "Show the view 2")\
                    .on_render("MY BEAUTIFUL VIEW 2") \
                .with_action("Back", "Back to the previous menu")\
                    .on_trigger(lambda x: x.parent) \
                .then() \
            .then() \
        .build()
    # fmt: on

    TUIMenuUi(main_menu, 'Testing Menus').execute()
