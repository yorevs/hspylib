from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame


class Panel(QFrame):

    keyPressed = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent=parent)

    def keyPressEvent(self, event):
        self.keyPressed.emit(event.key())
