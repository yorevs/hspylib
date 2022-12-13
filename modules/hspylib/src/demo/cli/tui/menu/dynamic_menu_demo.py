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
from hspylib.modules.cli.tui.menu.menu_factory import MenuFactory
from hspylib.modules.cli.tui.menu.menu_ui import MenuUi
from hspylib.modules.cli.vt100.vt_utils import exit_app

if __name__ == '__main__':
    # fmt: off
    main_menu = MenuFactory().INSTANCE \
        .create(None, 'Dynamic Main Menu') \
        .with_option('Exit').on_trigger(lambda t: exit_app(0)) \
        .with_option('Sub-Menu-1').on_trigger(lambda x: sub_menu_1) \
        .with_option('Sub-Menu-2').on_trigger(lambda x: sub_menu_2) \
        .build()
    sub_menu_1 = MenuFactory().INSTANCE \
        .create(main_menu, 'Sub-Menu-1') \
        .with_option('Back').on_trigger(lambda x: main_menu) \
        .with_option('Print Hey').on_trigger(lambda t: print('Hey')) \
        .with_option('Print Hoo').on_trigger(lambda t: print('Hoo')) \
        .build()
    sub_menu_2 = MenuFactory().INSTANCE \
        .create(main_menu, 'Sub-Menu-2') \
        .with_option('Back').on_trigger(lambda x: main_menu) \
        .with_option('Print Hello').on_trigger(lambda t: print('Hello')) \
        .with_option('Print Hi').on_trigger(lambda t: print('Hi')) \
        .build()
    # fmt: on
    mm = MenuUi(main_menu)
    mm.show()
