#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: kafka_consumer.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import threading
from time import sleep
from typing import List

from PyQt5.QtCore import pyqtSignal, QThread
from confluent_kafka.cimpl import Consumer

from hspylib.core.tools.commons import syserr


# Example at https://docs.confluent.io/platform/current/tutorials/examples/clients/docs/python.html
class KafkaConsumer(QThread):
    """TODO"""

    messageConsumed = pyqtSignal(str, int, int, bytes)

    def __init__(self, poll_interval: float = 0.5):
        super().__init__()
        self.setObjectName('kafka-consumer')
        self._started = False
        self._poll_interval = poll_interval
        self._consumer = None
        self._worker_thread = None
        self.start()

    def start_consumer(self, settings: dict) -> None:
        """TODO"""
        if self._consumer is None:
            self._consumer = Consumer(settings)
            self._started = True

    def stop_consumer(self) -> None:
        """TODO"""
        if self._consumer is not None:
            self._started = False

    def consume(self, topics: List[str]) -> None:
        """TODO"""
        if self._started:
            self._worker_thread = threading.Thread(target=self._consume, args=(topics,))
            self._worker_thread.name = f"kafka-consumer-worker-{hash(self)}"
            self._worker_thread.setDaemon(True)
            self._worker_thread.start()

    def is_started(self):
        """TODO"""
        return self._started

    def run(self) -> None:
        while not self.isFinished():
            sleep(self._poll_interval)

    def _consume(self, topics: List[str]) -> None:
        """TODO"""
        try:
            self._consumer.subscribe(topics)
            while self._started and self._consumer is not None:
                message = self._consumer.poll(self._poll_interval)
                if message is None:
                    continue
                elif message.error():
                    syserr(f"An error occurred consuming from Kafka: {message.error().str()}")
                else:
                    self.messageConsumed.emit(
                        message.topic(), message.partition(), message.offset(), message.value()
                    )
        except KeyboardInterrupt:
            syserr("Keyboard interrupted")
        finally:
            if self._consumer:
                self._consumer.close()
                del self._consumer
                self._consumer = None
                self._worker_thread = None
