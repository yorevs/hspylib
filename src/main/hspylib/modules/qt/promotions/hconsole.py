import typing

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QTextBrowser, QWidget

from hspylib.modules.eventbus.eventbus import EventBus


class HConsole(QTextBrowser):
    """TODO"""

    CONSOLE_BUS = 'console-bus'

    TEXT_DISPATCHED_EVT = 'console-text-dispatched'

    def __init__(self, parent: typing.Optional[QWidget]):
        super().__init__(parent)
        self.bus = EventBus.get(self.CONSOLE_BUS)
        self.setPlaceholderText('No messages received yet')
        self.setReadOnly(True)
        self.setFont(QFont("Courier New", 14))

    def put_text(self, text: str, color: QColor = None) -> None:
        fmt_text = f"<font color={color.name() if color else '#FFFFFF'}>{text}</font>"
        self.append(fmt_text)
