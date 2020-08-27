from main.hspylib.ui.cli.menu import Menu
from main.hspylib.ui.cli.menu_item import MenuItem
from main.hspylib.ui.cli.menu_utils import MenuUtils

MENU = """\033[2J\033[H
{}

\033[0;32m[0]\033[0;0;0m Back
\033[0;32m[1]\033[0;0;0m Print Hey
\033[0;32m[2]\033[0;0;0m Print Hoo
\033[0;32m[3]\033[0;0;0m Exit
"""


class SubMenu1(MenuItem):
    def __init__(self, parent: Menu = None):
        super().__init__(parent, '-= Sub Menu 1 =-')
        self.menu_data = str(MENU).format(self.title)
        self.options = range(0, 4)

    def trigger_menu_item(self) -> Menu:
        int_op = int(str(self.selected).strip())
        if int_op == 0:
            return self.parent
        elif int_op == 1:
            print('Hey')
        elif int_op == 2:
            print('Hoo')
        elif int_op == 3:
            MenuUtils.exit_app(0)

        return self
