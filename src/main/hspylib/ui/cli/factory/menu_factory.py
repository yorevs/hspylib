from main.hspylib.core.meta.singleton import Singleton
from main.hspylib.ui.cli.factory.menu_entry import MenuEntry
from main.hspylib.ui.cli.factory.menu_option import MenuOption
from main.hspylib.ui.cli.menu import Menu


class MenuFactory(metaclass=Singleton):
    INSTANCE = None

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

    def __init__(self):
        MenuFactory.INSTANCE = MenuFactory.INSTANCE if MenuFactory.INSTANCE else self

    @classmethod
    def create(cls, parent_menu: Menu = None, menu_title: str = None) -> MenuBuilder:
        return MenuFactory.MenuBuilder(parent_menu, menu_title)


MenuFactory.INSTANCE = MenuFactory()
