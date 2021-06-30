#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: kafka_producer.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import threading
from typing import List

from PyQt5.QtCore import pyqtSignal, QObject
from confluent_kafka.cimpl import Producer, KafkaError, Message

from hspylib.core.tools.commons import syserr


# Example at: # Example at https://docs.confluent.io/platform/current/tutorials/examples/clients/docs/python.html
class KafkaProducer(QObject):
    """TODO"""

    messageProduced = pyqtSignal(str, int, int, bytes)

    def __init__(self, poll_interval: float = 0.5, flush_timeout: int = 30):
        super().__init__()
        self._started = False
        self._poll_interval = poll_interval
        self._flush_timeout = flush_timeout
        self._producer = None
        self._worker_thread = None

    def flush(self, timeout: int = 0) -> None:
        """TODO"""
        if self._producer:
            self._producer.flush(timeout=timeout)

    def purge(self) -> None:
        """TODO"""
        if self._producer:
            self._producer.purge()

    def start(self, settings: dict) -> None:
        """TODO"""
        if self._producer is None:
            self._producer = Producer(settings)
            self._started = True

    def stop(self) -> None:
        """TODO"""
        if self._producer is not None:
            self.purge()
            self.flush()
            self._started = False
            del self._producer
            self._producer = None
            self._worker_thread = None

    def produce(self, topics: List[str], messages: List[str]) -> None:
        """TODO"""
        if self._started and self._producer is not None:
            self._worker_thread = threading.Thread(target=self._produce, args=(topics, messages,))
            self._worker_thread.name = 'kafka-producer'
            self._worker_thread.setDaemon(True)
            self._worker_thread.start()
            self._worker_thread.join()

    def is_started(self):
        """TODO"""
        return self._started

    def _produce(self, topics: List[str], messages: List[str]):
        """TODO"""
        try:
            for topic in topics:
                for msg in messages:
                    if msg:
                        self._producer.produce(topic, msg, callback=self._cb_message_produced)
                self._producer.poll(self._poll_interval)
        except KeyboardInterrupt:
            syserr("Keyboard interrupted")
        finally:
            self._producer.flush(self._flush_timeout)

    def _cb_message_produced(self, err: KafkaError, message: Message) -> None:
        """Delivery report handler called on successful or failed delivery of message"""
        if err is not None:
            syserr(f"Failed to deliver message: {err}")
        else:
            self.messageProduced.emit(
                message.topic(), message.partition(), message.offset(), message.value()
            )
