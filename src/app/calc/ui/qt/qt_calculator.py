
from PyQt5.QtWidgets import QApplication

from calc.ui.qt.views.main_ui import MainUi


class QtCalculator:
    def __init__(self):
        self.app = QApplication([])
        self.ui = MainUi()

    def run(self):
        self.ui.show()
        self.app.exec_()
