from abc import abstractmethod

from PyQt5 import uic
from hspylib.ui.qt.views.qt_view import QtView


class MainView(QtView):

    def __init__(self, ui_file_path: str):
        form, window = uic.loadUiType(ui_file_path)
        super().__init__(window)
        self.form = form
        self.form.setupUi(window)
        self.__setup_ui()

    @abstractmethod
    def __setup_ui(self) -> None:
        pass

    def show(self) -> None:
        self.window.show()
