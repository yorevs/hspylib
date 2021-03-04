from hspylib.ui.cli.menu.menu import Menu
from hspylib.ui.cli.menu.menu_item import MenuItem

MENU_TPL = """\033[2J\033[H
{}

{}
"""


class MenuEntry(MenuItem):
    def __init__(self, parent: Menu, items: dict, title: str = None):
        super().__init__(parent, title)
        title_len = round(len(title) / 2) + 2
        self.menu_data = MENU_TPL.format(
            '%ORANGE%{}\n  {}\n{}'.format('-='*title_len, self.title, '-='*title_len),
            '\n'.join([str(value) for key, value in items.items()])
        )
        self.options = range(0, len(items))
        self.items = items

    def trigger_menu_item(self) -> Menu:
        int_op = int(str(self.selected).strip())
        ret_val = self.items[str(int_op)].action_trigger(self)

        return ret_val if ret_val else self
