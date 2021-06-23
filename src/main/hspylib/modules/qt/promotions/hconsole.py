import threading
import typing
import collections
from time import sleep

from PyQt5.QtGui import QFont, QColor, QTextCursor
from PyQt5.QtWidgets import QWidget, QTextBrowser

from hspylib.modules.eventbus.eventbus import EventBus


class HConsole(QTextBrowser):
    """TODO"""

    CONSOLE_BUS = 'console-bus'

    TEXT_DISPATCHED_EVT = 'console-text-dispatched'

    REFRESH_INTERVAL = 1

    MAX_BUFFER_SIZE = 1000

    MAX_LEN_PER_REFRESH = 10

    def __init__(self, parent: typing.Optional[QWidget]):
        super().__init__(parent)
        self._bus = EventBus.get(self.CONSOLE_BUS)
        self._deque = collections.deque(maxlen=self.MAX_BUFFER_SIZE)
        self._started = False
        self._textCursor = self.textCursor()
        self.setPlaceholderText('No messages received yet')
        self.setReadOnly(True)
        self.setFont(QFont("Courier New", 14))
        self._start()

    def put_text(self, text: str, color: QColor = None) -> None:
        """TODO"""
        fmt_text = f"<font color={color.name() if color else '#FFFFFF'}>{text}</font>"
        self._deque.append(fmt_text)

    def _start(self):
        if not self._started:
            self._started = True
            tr = threading.Thread(target=self._refresh)
            tr.setDaemon(True)
            tr.start()

    def _stop(self):
        if self._started:
            self._started = False

    def _refresh(self):
        while self._started:
            sleep(HConsole.REFRESH_INTERVAL)
            if self._deque:
                size = range(0, len(self._deque))
                for _ in size:
                    print(self._deque.popleft())
