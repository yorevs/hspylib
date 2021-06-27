from typing import Optional

from PyQt5.QtWidgets import QComboBox, QWidget


class HComboBox(QComboBox):

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)

    def set_item(self, item: str) -> None:
        """TODO"""
        if self.findText(item) < 0:
            self.addItem(item)
