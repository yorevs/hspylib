from abc import ABC
from typing import TypeVar

from PyQt5.QtWidgets import QApplication

V = TypeVar('V')


class QtApplication(ABC):

    def __init__(self, main_view: V):
        super().__init__()
        self.app = QApplication([])
        self.main_view = main_view()

    def run(self) -> int:
        """Show the main Qt application Widget"""
        self.main_view.show()
        return self.app.exec_()
