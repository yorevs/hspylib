from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


class ButtonLabel(QLabel):

    clicked = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent=parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()
