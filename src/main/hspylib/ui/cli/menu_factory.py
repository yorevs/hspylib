from main.hspylib.core.meta.singleton import Singleton
from main.hspylib.ui.cli.menu import Menu
from main.hspylib.ui.cli.menu_item import MenuItem

MENU_TPL = """\033[2J\033[H
{}

{}
"""


class MenuOption:
    def __init__(self, parent, option_index: int, option_text: str):
        self.parent = parent
        self.option_index = option_index
        self.option_text = option_text
        self.action_trigger = lambda s: print(f"Option: {self.option_index}-{self.option_text} selected!")

    def on_trigger(self, action_trigger):
        self.action_trigger = action_trigger
        return self.parent

    def __str__(self):
        return "\033[0;32m[{}]\033[0;0;0m {}".format(self.option_index, self.option_text)


class DynamicMenuItem(MenuItem):
    def __init__(self, parent: Menu, items: dict, title: str = None):
        super().__init__(parent, title)
        self.menu_data = MENU_TPL.format(self.title, '\n'.join([str(value) for key, value in items.items()]))
        self.options = range(0, len(items))
        self.items = items

    def trigger_menu_item(self) -> Menu:
        int_op = int(str(self.selected).strip())
        ret_val = self.items[str(int_op)].action_trigger(self)

        return ret_val if ret_val else self


class MenuBuilder:
    def __init__(self, parent_menu: Menu = None, menu_title: str = None):
        self.parent_menu = parent_menu
        self.menu_title = menu_title
        self.menu_options = {}

    def with_option(self, option_index: int, option_text: str) -> MenuOption:
        option = MenuOption(self, option_index, option_text)
        self.menu_options[str(option_index)] = option
        return option

    def build(self) -> Menu:
        return DynamicMenuItem(self.parent_menu, self.menu_options, self.menu_title)


class MenuFactory(metaclass=Singleton):
    INSTANCE = None

    def __init__(self):
        MenuFactory.INSTANCE = MenuFactory.INSTANCE if MenuFactory.INSTANCE else self

    @classmethod
    def create(cls, parent_menu: Menu = None, menu_title: str = None) -> MenuBuilder:
        return MenuBuilder(parent_menu, menu_title)


MenuFactory.INSTANCE = MenuFactory()
