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
import sys

from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version
from hspylib.modules.cli.cli_application import CliApplication
from hspylib.modules.cli.tui.menu.tui_menu_factory import TUIMenuFactory
from hspylib.modules.cli.tui.menu.tui_menu_ui import TUIMenuUi

from phonebook.__classpath__ import _Classpath
from phonebook.view.create_view import CreateView
from phonebook.view.edit_view import EditView
from phonebook.view.search_view import SearchView


class Main(CliApplication):
    """TODO"""

    def __init__(self, app_name: str):
        version = Version.load(load_dir=_Classpath.run_path())
        super().__init__(app_name, version, "A Simple CLI phonebook", resource_dir=str(_Classpath.resource_path()))

    def _main(self, *args, **kwargs) -> ExitStatus:  # pylint: disable=unused-argument
        create_view, edit_view, search_view = CreateView(), EditView(), SearchView()
        # fmt: off
        main_menu = TUIMenuFactory \
            .create_main_menu(self._app_name, 'Main Menu') \
                .with_item('Create', 'Create new contact') \
                    .with_action('Back', 'Back to previous menu') \
                        .on_trigger(lambda x: x.parent) \
                    .with_view('Person', 'Create a new Person contact') \
                        .on_render(lambda : create_view.person()) \
                    .with_view('Company', 'Create a new Company contact') \
                        .on_render(lambda : create_view.company()) \
                    .then() \
                .with_item('Edit', 'Edit contact') \
                    .with_action('Back', 'Back to previous menu') \
                        .on_trigger(lambda x: x.parent) \
                    .with_view('Person', 'Edit a Person contact') \
                        .on_render(lambda : edit_view.person()) \
                    .with_view('Company', 'Edit a Company contact') \
                        .on_render(lambda : edit_view.company()) \
                    .then() \
                .with_item('Search', 'Search contacts') \
                    .with_action('Back', 'Back to previous menu') \
                        .on_trigger(lambda x: x.parent) \
                    .with_view('By name', 'Search contacts by name') \
                        .on_render(lambda : search_view.by_name()) \
                    .with_view('By uid', 'Search contacts by user ID') \
                        .on_render(lambda : search_view.by_uuid()) \
                    .with_view('List all', 'List all available contacts') \
                        .on_render(lambda : search_view.list_all()) \
                    .then() \
                .then() \
            .build()
        # fmt: on
        TUIMenuUi(main_menu).execute('Phonebook')
        return ExitStatus.SUCCESS


# Application entry point
if __name__ == "__main__":
    # Application entry point
    Main("HSPyLib Phonebook - Demo").INSTANCE.run(sys.argv[1:])
