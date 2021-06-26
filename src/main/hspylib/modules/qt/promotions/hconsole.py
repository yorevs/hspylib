import typing

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QTextCursor, QCursor
from PyQt5.QtWidgets import QWidget, QTextBrowser


class HConsole(QTextBrowser):
    """TODO"""

    def __init__(self, parent: typing.Optional[QWidget], buffer_size: int = 1000):
        super().__init__(parent)
        self.setPlaceholderText('No messages received yet')
        self.setReadOnly(True)
        self.setFont(QFont("Courier New", 14))
        self._buffer_size = buffer_size
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._context_menu)

    def line_count(self) -> int:
        """Return the number of lines the console contains"""
        return self.document().blockCount()

    def push_text(self, text: str, color: QColor = None) -> None:
        """Push text to the console. If the maximum buffer size reached,
           the first lines are erased
        """
        fmt_text = f"<font color={color.name() if color else '#FFFFFF'}>{text}</font>"
        if self.line_count() + 1 > self._buffer_size:
            self.pop_text()
        self.append(fmt_text)

    def pop_text(self, count: int = 0) -> str:
        """Pop <count> lines form the top->bottom"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, count)
        cursor.select(QTextCursor.LineUnderCursor)
        selected_text = cursor.selectedText()
        cursor.removeSelectedText()
        cursor.deleteChar()
        self.setTextCursor(cursor)

        return selected_text

    def _context_menu(self):
        """Display the custom context menu"""
        self._menu = self.createStandardContextMenu()
        self._menu.addSeparator()
        self._menu.addAction(u'Clear', self.clear)
        self._menu.exec_(QCursor.pos())
