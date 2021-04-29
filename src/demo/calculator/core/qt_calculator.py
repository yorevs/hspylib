
from PyQt5.QtWidgets import QApplication

from calculator.ui.qt.views.main_view import MainView


class QtCalculator:
    def __init__(self):
        self.app = QApplication([])
        self.ui = MainView()

    def show(self):
        self.ui.show()
        self.app.exec_()
