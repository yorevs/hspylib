import signal

from main.hspylib.ui.cli.menu import Menu
from main.hspylib.ui.cli.menu_utils import MenuUtils
from main.hspylib.ui.cli.sample.main_menu import MainMenu


class MenuUi:
    def __init__(self, main_menu: Menu):
        self.done = False
        self.previous = None
        self.current = main_menu
        self.next = None
        signal.signal(signal.SIGINT, MenuUtils.exit_app)

    def run(self) -> None:
        while not self.done:
            if self.current:
                self.next = self.current.execute()
                if self.next is None:
                    self.done = True
                else:
                    self.change_menu(self.next)
            else:
                self.done = True

    def change_menu(self, menu: Menu) -> None:
        self.previous = self.current
        self.current = menu


if __name__ == '__main__':
    mm = MenuUi(MainMenu())
    mm.run()
