#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: kafka_statistics.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Tuple

from PyQt5.QtCore import QThread, pyqtSignal

from hspylib.core.tools.commons import now_ms


class KafkaStatistics(QThread):
    """TODO"""

    statisticsReported = pyqtSignal(int, int, int, int, int, int)

    class ConsumerStats:
        """Gather consumer statistics"""

        def __init__(self):
            self.total = 0
            self.in_a_tick = 0

    class ProducerStats:
        """Gather producer statistics"""

        def __init__(self):
            self.total = 0
            self.in_a_tick = 0

    def __init__(self, report_interval: int = 1):
        super().__init__()
        self.setObjectName('kafka-statistics')
        self._started_ts = now_ms()
        self._consumed = self.ConsumerStats()
        self._produced = self.ProducerStats()
        self._report_interval = report_interval

    def report_consumed(self, amount: int = 1) -> None:
        """Report a consumed message"""
        self._consumed.in_a_tick += amount
        self._consumed.total += amount

    def report_produced(self, amount: int = 1) -> None:
        """Report a produced message"""
        self._produced.in_a_tick += amount
        self._produced.total += amount

    def get_total(self) -> Tuple[int, int]:
        """Retrieve the totals produced/consumed so far"""
        return self._produced.total, self._consumed.total

    def get_in_a_tick(self) -> Tuple[int, int]:
        """Retrieve the amount produced/consumed in a tick"""
        return self._produced.in_a_tick, self._consumed.in_a_tick

    def run(self) -> None:
        while not self.isFinished():
            self.sleep(self._report_interval)
            self._tick()

    def _tick(self) -> None:
        """TODO"""
        diff_time = max(1, int(now_ms() - self._started_ts))
        self._produced.in_a_tick = 0
        self._consumed.in_a_tick = 0
        self.statisticsReported.emit(
            self._produced.total,
            self._consumed.total,
            self._produced.in_a_tick,
            self._consumed.in_a_tick,
            int(self._produced.total / diff_time),
            int(self._consumed.total / diff_time)
        )
