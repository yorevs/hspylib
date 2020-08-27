from main.hspylib.ui.cli.menu_ui import MenuUi
from main.hspylib.ui.cli.sample.main_menu import MainMenu

if __name__ == '__main__':
    mm = MenuUi(MainMenu())
    mm.run()
