import io
from contextlib import redirect_stdout, redirect_stderr
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from hspylib.core.tools.commons import is_debugging


class StreamCapturer(QThread):
    """QThread to captures stdout and/or stderr messages and send them via PyQt Signal"""

    stdoutCaptured = pyqtSignal(str)
    stderrCaptured = pyqtSignal(str)

    class StdoutWorker(QThread):
        """QThread worker to capture stdout messages"""
        streamCaptured = pyqtSignal(str)
        def __init__(self, parent, poll_interval: float):
            super().__init__()
            self._poll_interval = poll_interval
            self._parent = parent

        def run(self):
            self.setObjectName('stdout-worker')
            with io.StringIO() as buf, redirect_stdout(buf):
                while not self._parent.isFinished():
                    output = buf.getvalue()
                    if output and output != '':
                        self.streamCaptured.emit(output)
                        buf.truncate(0)
                    sleep(self._poll_interval)

    class StderrWorker(QThread):
        """QThread worker to capture stderr messages"""
        streamCaptured = pyqtSignal(str)
        def __init__(self, parent, poll_interval: float):
            super().__init__()
            self._poll_interval = poll_interval
            self._parent = parent

        def run(self):
            self.setObjectName('stderr-worker')
            with io.StringIO() as buf, redirect_stderr(buf):
                while not self._parent.isFinished():
                    output = buf.getvalue()
                    if output and output != '':
                        self.streamCaptured.emit(output)
                        buf.truncate(0)
                    sleep(self._poll_interval)

    def __init__(self, stdout_poll_interval: float = 0.5, stderr_poll_interval: float = 0.5):
        super().__init__()
        self.setObjectName('stream-capturer')
        self._stderr_capturer = self.StderrWorker(self, stderr_poll_interval)
        self._stdout_capturer = self.StdoutWorker(self, stdout_poll_interval)
        self._stderr_capturer.streamCaptured.connect(lambda msg: self.stderrCaptured.emit(msg))
        self._stdout_capturer.streamCaptured.connect(lambda msg: self.stdoutCaptured.emit(msg))
        self._poll_interval = stdout_poll_interval + stderr_poll_interval

    def run(self) -> None:
        self._stderr_capturer.start()
        self._stdout_capturer.start()
        while not self.isFinished():
            sleep(self._poll_interval)

    def start(self, priority: QThread.Priority = QThread.NormalPriority) -> None:
        if not is_debugging():
            super().start(priority)
