from hspylib.ui.cli.menu.menu import Menu
from hspylib.ui.cli.menu.menu_item import MenuItem
from hspylib.ui.cli.menu.menu_utils import MenuUtils

MENU = """%VT_ED2%%VT_HOM%
{}

%GREEN%[0]%NC% Back
%GREEN%[1]%NC% Print Hey
%GREEN%[2]%NC% Print Hoo
%GREEN%[3]%NC% Exit
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
