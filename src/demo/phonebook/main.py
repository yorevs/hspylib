#!/usr/bin/env python
import os
import signal

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.ui.cli.menu_ui import MenuUi

from hspylib.ui.cli.menu_utils import MenuUtils

from hspylib.ui.cli.factory.menu_factory import MenuFactory
from phonebook.view.create_view import CreateView
from phonebook.view.edit_view import EditView
from phonebook.view.search_view import SearchView


class Main(metaclass=Singleton):

    @staticmethod
    def exit_app(sig=None, frame=None) -> None:
        sysout(frame if frame else '', end='')
        sysout('\033[2J\033[H')
        exit(sig)

    def __init__(self):
        source_dir = os.path.dirname(os.path.realpath(__file__))
        resource_dir = '{}/resources'.format(source_dir)
        log_dir = '{}/log'.format(resource_dir)
        self.configs = AppConfigs(
            source_root=source_dir,
            resource_dir=resource_dir,
            log_dir=log_dir
        )
        self.configs.logger().info(self.configs)

    @staticmethod
    def run() -> None:
        create_view = CreateView()
        edit_view = EditView()
        search_view = SearchView()
        main_menu = MenuFactory \
            .create(None, 'HSPYLIB Demo Phonebook') \
            .with_option('Exit').on_trigger(lambda t: MenuUtils.exit_app(0)) \
            .with_option('Create').on_trigger(lambda x: create_menu) \
            .with_option('Edit').on_trigger(lambda x: edit_menu) \
            .with_option('Search').on_trigger(lambda x: search_menu) \
            .build()
        create_menu = MenuFactory \
            .create(main_menu, 'Create new contact') \
            .with_option('Back').on_trigger(lambda x: main_menu) \
            .with_option('Person').on_trigger(lambda t: create_view.person()) \
            .with_option('Company').on_trigger(lambda t: create_view.company()) \
            .build()
        edit_menu = MenuFactory \
            .create(main_menu, 'Edit contact') \
            .with_option('Back').on_trigger(lambda x: main_menu) \
            .with_option('Person').on_trigger(lambda t: edit_view.person()) \
            .with_option('Company').on_trigger(lambda t: edit_view.company()) \
            .build()
        search_menu = MenuFactory \
            .create(main_menu, 'Search contacts') \
            .with_option('Back').on_trigger(lambda x: main_menu) \
            .with_option('By name').on_trigger(lambda t: search_view.by_name()) \
            .with_option('By uuid').on_trigger(lambda t: search_view.by_uuid()) \
            .with_option('List all').on_trigger(lambda t: search_view.list_all()) \
            .build()
        mm = MenuUi(main_menu)
        mm.run()


# Application entry point
if __name__ == "__main__":
    signal.signal(signal.SIGINT, Main.exit_app)
    Main().INSTANCE.run()
    Main.exit_app(0)
