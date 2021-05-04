from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QWidget

from hspylib.modules.qt.qt_finder import QtFinder


class QtView(ABC):
    def __init__(self, window: QWidget, parent=None):
        super().__init__()
        self.window = window
        self.parent = parent
        self.qt = QtFinder(self.window)

    @abstractmethod
    def setup_ui(self):
        pass
