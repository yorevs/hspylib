#!/usr/bin/env python3
from hspylib.ui.cli.menu.menu_ui import MenuUi
from ui.cli.menu.main_menu import MainMenu

if __name__ == '__main__':
    mm = MenuUi(MainMenu())
    mm.run()
