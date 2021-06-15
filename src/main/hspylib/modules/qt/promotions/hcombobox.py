from PyQt5.QtWidgets import QComboBox


class HComboBox(QComboBox):

    def __init__(self, parent):
        super().__init__(parent=parent)

    def set_item(self, item: str) -> None:
        """TODO"""
        if self.findText(item) < 0:
            self.addItem(item)
