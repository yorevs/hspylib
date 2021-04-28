#!/usr/bin/env python3
import sys

from hspylib.ui.cli.app.application import Application
from hspylib.ui.cli.factory.menu_factory import MenuFactory
from hspylib.ui.cli.menu.menu_ui import MenuUi
from hspylib.ui.cli.menu.menu_utils import MenuUtils
from phonebook.view.create_view import CreateView
from phonebook.view.edit_view import EditView
from phonebook.view.search_view import SearchView


class Main(Application):

    def __init__(self, app_name: str):
        super().__init__(app_name, (0, 9, 0))

    def main(self, *args, **kwargs) -> None:
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
        mm.run()


# Application entry point
if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Phonebook Demo').INSTANCE.run(sys.argv[1:])
