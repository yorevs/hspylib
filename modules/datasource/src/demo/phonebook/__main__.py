#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version
from hspylib.modules.cli.cli_application import CliApplication
from hspylib.modules.cli.tui.menu.menu_factory import MenuFactory
from hspylib.modules.cli.tui.menu.menu_ui import MenuUi
from hspylib.modules.cli.vt100.vt_utils import exit_app
from phonebook.__classpath__ import _Classpath
from phonebook.view.create_view import CreateView
from phonebook.view.edit_view import EditView
from phonebook.view.search_view import SearchView

import sys


class Main(CliApplication):
    """TODO"""

    def __init__(self, app_name: str):
        version = Version.load(load_dir=_Classpath.run_path())
        super().__init__(
            app_name, version, 'A Simple CLI phonebook',
            resource_dir=str(_Classpath.resource_path()))

    def _main(self, *args, **kwargs) -> ExitStatus:  # pylint: disable=unused-argument
        create_view, edit_view, search_view = CreateView(), EditView(), SearchView()
        # @formatter:off
        main_menu = MenuFactory \
            .create(menu_title=self._app_name) \
                .with_option('Exit')\
                    .on_trigger(lambda t: exit_app(0)) \
                .with_option('Create')\
                    .on_trigger(lambda x: create_menu) \
                .with_option('Edit')\
                    .on_trigger(lambda x: edit_menu) \
                .with_option('Search')\
                    .on_trigger(lambda x: search_menu) \
                .build()
        create_menu = MenuFactory \
            .create(parent_menu=main_menu, menu_title='Create new contact') \
                .with_option('Back')\
                    .on_trigger(lambda x: main_menu) \
                .with_option('Person')\
                    .on_trigger(lambda t: create_view.person()) \
                .with_option('Company')\
                    .on_trigger(lambda t: create_view.company()) \
                .build()
        edit_menu = MenuFactory \
            .create(parent_menu=main_menu, menu_title='Edit contact') \
                .with_option('Back')\
                    .on_trigger(lambda x: main_menu) \
                .with_option('Person')\
                    .on_trigger(lambda t: edit_view.person()) \
                .with_option('Company')\
                    .on_trigger(lambda t: edit_view.company()) \
                .build()
        search_menu = MenuFactory \
            .create(parent_menu=main_menu, menu_title='Search contacts') \
                .with_option('Back')\
                    .on_trigger(lambda x: main_menu) \
                .with_option('By name')\
                    .on_trigger(lambda t: search_view.by_name()) \
                .with_option('By uid')\
                    .on_trigger(lambda t: search_view.by_uuid()) \
                .with_option('List all')\
                    .on_trigger(lambda t: search_view.list_all()) \
                .build()
        # @formatter:on
        mm = MenuUi(main_menu)
        mm.show()
        return ExitStatus.SUCCESS


# Application entry point
if __name__ == "__main__":
    # Application entry point
    Main('HSPyLib Phonebook - Demo').INSTANCE.run(sys.argv[1:])
