#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: statistics.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import threading
from time import sleep

from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import now_ms
from hspylib.modules.eventbus.eventbus import EventBus


class Statistics(metaclass=Singleton):
    """TODO"""

    REPORT_INTERVAL = 1

    class ConsumerStats:
        """TODO"""
        def __init__(self):
            self.total = 0
            self.in_a_tick = 0

    class ProducerStats:
        """TODO"""
        def __init__(self):
            self.total = 0
            self.in_a_tick = 0

    def __init__(self):
        self._started_ts = now_ms()
        self._consumed = self.ConsumerStats()
        self._produced = self.ProducerStats()
        self._bus = EventBus.get('kafka-statistics')
        tr = threading.Thread(target=self._report)
        tr.setDaemon(True)
        tr.start()

    def consumed(self, amount: int = 1) -> None:
        """TODO"""
        self._consumed.in_a_tick += amount
        self._consumed.total += amount

    def produced(self, amount: int = 1) -> None:
        """TODO"""
        self._produced.in_a_tick += amount
        self._produced.total += amount

    def _report(self) -> None:
        """TODO"""
        while True:
            diff_time = max(1, int(now_ms() - self._started_ts))
            stats = \
                self._produced.total, \
                self._consumed.total, \
                self._produced.in_a_tick, \
                self._consumed.in_a_tick, \
                int(self._produced.total / diff_time), \
                int(self._consumed.total / diff_time)
            self._produced.in_a_tick = 0
            self._consumed.in_a_tick = 0
            self._bus.emit('stats-report', stats=stats)
            sleep(self.REPORT_INTERVAL)
