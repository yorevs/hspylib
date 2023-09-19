#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: stream_capturer.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import io
import logging as log
import sys
from contextlib import redirect_stdout, redirect_stderr
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from hspylib.core.tools.commons import is_debugging, syserr


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
            self.setObjectName(f"stdout-worker-{hash(self)}")
            with io.StringIO() as buf, redirect_stdout(buf):
                while not self._parent.isFinished():
                    output = buf.getvalue()
                    if output and output != '':
                        log.debug(output)
                        self.streamCaptured.emit(output)
                        print(output, file=sys.__stdout__)
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
                        log.error(output)
                        self.streamCaptured.emit(output)
                        print(output, file=sys.__stderr__)
                        buf.truncate(0)
                    sleep(self._poll_interval)

    def __init__(
            self,
            capture_stderr: bool = True,
            capture_stdout: bool = True,
            stdout_poll_interval: float = 0.5,
            stderr_poll_interval: float = 0.5):

        assert capture_stderr or capture_stdout, 'At least one capturer must be started'
        super().__init__()
        self.setObjectName('stream-capturer')
        self._capture_stdout = capture_stdout
        self._capture_stderr = capture_stderr
        self._poll_interval = stdout_poll_interval + stderr_poll_interval

        if self._capture_stderr:
            self._stderr_capturer = self.StderrWorker(self, stderr_poll_interval)
            self._stderr_capturer.streamCaptured.connect(lambda msg: self.stderrCaptured.emit(msg))
        if self._capture_stdout:
            self._stdout_capturer = self.StdoutWorker(self, stdout_poll_interval)
            self._stdout_capturer.streamCaptured.connect(lambda msg: self.stdoutCaptured.emit(msg))

    def run(self) -> None:

        if self._capture_stderr:
            self._stderr_capturer.start()
        if self._capture_stdout:
            self._stdout_capturer.start()

        while not self.isFinished():
            sleep(self._poll_interval)

    def start(self, priority: QThread.Priority = QThread.NormalPriority) -> None:
        if not is_debugging():
            super().start(priority)
        else:
            syserr('Stderr/Stdout capture is not started in debugging mode')
