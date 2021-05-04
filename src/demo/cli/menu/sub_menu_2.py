from hspylib.modules.cli.menu.menu import Menu
from hspylib.modules.cli.menu.menu_item import MenuItem

MENU = """%ED2%%HOM%
{}

%GREEN%[0]%NC% Back
%GREEN%[1]%NC% Print Hello
%GREEN%[2]%NC% Print Hi
"""


class SubMenu2(MenuItem):
    def __init__(self, parent: Menu = None):
        super().__init__(parent, '-= Sub Menu 2 =-')
        self.menu_data = str(MENU).format(self.title)
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
