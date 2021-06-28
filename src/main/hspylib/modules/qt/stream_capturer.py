import io
from contextlib import redirect_stdout, redirect_stderr
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from kafman.src.main.core.constants import POLLING_INTERVAL


class StreamCapturer(QThread):
    """TODO"""

    stdoutCaptured = pyqtSignal(str)
    stderrCaptured = pyqtSignal(str)

    class StdoutWorker(QThread):
        """TODO"""
        streamCaptured = pyqtSignal(str)
        def run(self):
            self.setObjectName("stdout-worker")
            with io.StringIO() as buf, redirect_stdout(buf):
                while True:
                    output = buf.getvalue()
                    if output and output != '':
                        self.streamCaptured.emit(output)
                        buf.truncate()
                    sleep(POLLING_INTERVAL)

    class StderrWorker(QThread):
        """TODO"""
        streamCaptured = pyqtSignal(str)
        def run(self):
            self.setObjectName("stderr-worker")
            with io.StringIO() as buf, redirect_stderr(buf):
                while True:
                    output = buf.getvalue()
                    if output and output != '':
                        self.streamCaptured.emit(output)
                        buf.truncate()
                    sleep(POLLING_INTERVAL)

    def __init__(self):
        super().__init__()
        self._stderr_capturer = self.StderrWorker()
        self._stdout_capturer = self.StdoutWorker()
        self._stderr_capturer.streamCaptured.connect(lambda msg: self.stderrCaptured.emit(msg))
        self._stdout_capturer.streamCaptured.connect(lambda msg: self.stdoutCaptured.emit(msg))

    def run(self):
        print('Started capturing stdout and stderr')
        self._stderr_capturer.start()
        self._stdout_capturer.start()
        self._stderr_capturer.wait()
        self._stdout_capturer.wait()
