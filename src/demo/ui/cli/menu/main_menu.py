from hspylib.ui.cli.menu.menu import Menu
from hspylib.ui.cli.menu.menu_item import MenuItem
from hspylib.ui.cli.menu.menu_utils import MenuUtils
from ui.cli.menu.sub_menu_1 import SubMenu1
from ui.cli.menu.sub_menu_2 import SubMenu2

MENU = """%ED2%%HOM%
{}

%GREEN%[0]%NC% Exit
%GREEN%[1]%NC% Sub Menu 1
%GREEN%[2]%NC% Sub Menu 2
"""


class MainMenu(MenuItem):
    def __init__(self):
        super().__init__(title='Static Main Menu')
        self.menu_data = str(MENU).format(self.title)
        self.options = range(0, 3)
        self.menu_items = {
            '1': SubMenu1(parent=self),
            '2': SubMenu2(parent=self)
        }

    def trigger_menu_item(self) -> Menu:
        int_op = int(str(self.selected).strip())
        if int_op == 0:
            MenuUtils.exit_app(0)
        else:
            return self.menu_items[str(int_op)]
