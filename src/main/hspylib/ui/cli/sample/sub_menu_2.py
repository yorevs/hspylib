from main.hspylib.ui.cli.menu import Menu
from main.hspylib.ui.cli.menu_item import MenuItem

MENU = """\033[2J\033[H
\033[0;32m[0]\033[0;0;0m Back
\033[0;32m[1]\033[0;0;0m Print Hello
\033[0;32m[2]\033[0;0;0m Print Hi
"""


class SubMenu2(MenuItem):
    def __init__(self, parent: Menu = None):
        super().__init__(parent)
        self.menu_data = str(MENU)
        self.options = range(0, 3)

    def trigger_menu_item(self) -> Menu:
        int_op = int(str(self.selected).strip())
        if int_op == 0:
            return self.parent
        elif int_op == 1:
            print('Hello')
        elif int_op == 2:
            print('Hi')

        return self
