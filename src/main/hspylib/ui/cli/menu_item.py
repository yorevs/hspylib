from abc import ABC
from typing import Optional

from main.hspylib.ui.cli.menu_utils import MenuUtils
from main.hspylib.ui.cli.menu import Menu


class MenuItem(Menu, ABC):
    def __init__(self, parent: Menu = None):
        self.parent = parent
        self.done = False
        self.selected = None
        self.items = None
        self.options = None
        self.menu_data = None

    def __str__(self):
        return self.menu_data if self.menu_data else ''

    def execute(self) -> Optional[Menu]:
        while not self.selected == 0 and not self.done:
            print(self)
            self.selected = MenuUtils.prompt()
            if not self.selected:
                return None
            elif self.selected.isalnum() and self.is_valid_option():
                return self.trigger_menu_item()
            else:
                MenuUtils.print_error("Invalid option", self.selected)
                self.selected = None

    def trigger_menu_item(self) -> Optional[Menu]:
        return None

    def is_valid_option(self) -> bool:
        if not self.options or not self.selected:
            return False
        elif self.selected.isdigit():
            return int(self.selected) in self.options
        else:
            return str(self.selected) in self.options
