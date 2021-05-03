from hspylib.core.meta.singleton import Singleton
from hspylib.ui.cli.menu.factory.menu_entry import MenuEntry
from hspylib.ui.cli.menu.factory.menu_option import MenuOption
from hspylib.ui.cli.menu.menu import Menu


class MenuFactory(metaclass=Singleton):

    class MenuBuilder:
        def __init__(self, parent_menu: Menu = None, menu_title: str = None):
            self.parent_menu = parent_menu
            self.menu_title = menu_title
            self.menu_options = {}

        def with_option(self, option_text: str) -> MenuOption:
            option_index = len(self.menu_options)
            option = MenuOption(self, option_index, option_text)
            self.menu_options[str(option_index)] = option
            return option

        def build(self) -> Menu:
            return MenuEntry(self.parent_menu, self.menu_options, self.menu_title)

    @staticmethod
    def create(parent_menu: Menu = None, menu_title: str = None) -> MenuBuilder:
        return MenuFactory.MenuBuilder(parent_menu, menu_title)
