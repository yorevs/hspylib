#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.demo.phonebook
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys
from hspylib.core.tools.commons import dirname
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.menu.factory.menu_factory import MenuFactory
from hspylib.modules.cli.menu.menu_ui import MenuUi
from hspylib.modules.cli.menu.menu_utils import MenuUtils
from phonebook.view.create_view import CreateView
from phonebook.view.edit_view import EditView
from phonebook.view.search_view import SearchView



class Main(Application):
    """TODO"""
    
    # Version tuple: (major,minor,build)
    VERSION = (0, 9, 0)
    
    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, source_dir=dirname(__file__))
    
    def _main(self, *args, **kwargs) -> None:  # pylint: disable=unused-argument
        create_view = CreateView()
        edit_view = EditView()
        search_view = SearchView()
        main_menu = MenuFactory \
            .create(menu_title='HSPYLIB Demo Phonebook') \
            .with_option('Exit').on_trigger(lambda t: MenuUtils.exit_app(0)) \
            .with_option('Create').on_trigger(lambda x: create_menu) \
            .with_option('Edit').on_trigger(lambda x: edit_menu) \
            .with_option('Search').on_trigger(lambda x: search_menu) \
            .build()
        create_menu = MenuFactory \
            .create(parent_menu=main_menu, menu_title='Create new contact') \
            .with_option('Back').on_trigger(lambda x: main_menu) \
            .with_option('Person').on_trigger(lambda t: create_view.person()) \
            .with_option('Company').on_trigger(lambda t: create_view.company()) \
            .build()
        edit_menu = MenuFactory \
            .create(parent_menu=main_menu, menu_title='Edit contact') \
            .with_option('Back').on_trigger(lambda x: main_menu) \
            .with_option('Person').on_trigger(lambda t: edit_view.person()) \
            .with_option('Company').on_trigger(lambda t: edit_view.company()) \
            .build()
        search_menu = MenuFactory \
            .create(parent_menu=main_menu, menu_title='Search contacts') \
            .with_option('Back').on_trigger(lambda x: main_menu) \
            .with_option('By name').on_trigger(lambda t: search_view.by_name()) \
            .with_option('By uuid').on_trigger(lambda t: search_view.by_uuid()) \
            .with_option('List all').on_trigger(lambda t: search_view.list_all()) \
            .build()
        mm = MenuUi(main_menu)
        mm.show()


# Application entry point
if __name__ == "__main__":
    # Application entry point
    Main('HSPyLib Phonebook Demo').INSTANCE.run(sys.argv[1:])
