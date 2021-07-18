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
from hspylib.modules.qt.kafka.schemas.kafka_avro_schema import KafkaAvroSchema

from hspylib.core.tools.commons import syserr


# Example at https://docs.confluent.io/platform/current/tutorials/examples/clients/docs/python.html
# For all kafka settings: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
class KafkaConsumer(QThread):
    """TODO"""

    plainMessageConsumed = pyqtSignal(str, int, int, bytes)
    avroMessageConsumed = pyqtSignal(str, int, int, bytes)

    def __init__(self, poll_interval: float = 0.5):
        super().__init__()
        self.setObjectName('kafka-consumer')
        self._started = False
        self._poll_interval = poll_interval
        self._schema = None
        self._consumer = None
        self._worker_thread = None
        self.start()

    def start_consumer(self, settings: dict) -> None:
        """Start the Kafka consumer agent"""
        if self._consumer is None:
            self._consumer = Consumer(settings)
            self._started = True

    def stop_consumer(self) -> None:
        """Stop the Kafka consumer agent"""
        if self._consumer is not None:
            self._started = False
            del self._consumer
            self._consumer = None
            self._worker_thread = None
            self._schema = None

    def consume(self, topics: List[str]) -> None:
        """Start the consumer thread"""
        if self._started:
            self._worker_thread = threading.Thread(target=self._consume, args=(topics,))
            self._worker_thread.name = f"kafka-consumer-worker-{hash(self)}"
            self._worker_thread.setDaemon(True)
            self._worker_thread.start()

    def set_schema(self, schema: KafkaAvroSchema) -> None:
        self._schema = schema

    def is_started(self) -> bool:
        """Whether the consumer is started or not"""
        return self._started

    def run(self) -> None:
        while not self.isFinished():
            sleep(self._poll_interval)

    def _consume(self, topics: List[str]) -> None:
        """Consume messages from the selected Kafka topics"""
        try:
            self._consumer.subscribe(topics)
            while self._started and self._consumer is not None:
                message = self._consumer.poll(self._poll_interval)
                if message is None:
                    continue
                if message.error():
                    syserr(f"An error occurred consuming from Kafka: {message.error().str()}")
                else:
                    if not self._schema:
                        self.plainMessageConsumed.emit(
                            message.topic(), message.partition(), message.offset(), message.value())
                    else:
                        self.avroMessageConsumed.emit(
                            message.topic(), message.partition(), message.offset(),
                            self._schema.decode(message.value()))
        except KeyboardInterrupt:
            syserr("Keyboard interrupted")
        finally:
            if self._consumer:
                self._consumer.close()
                del self._consumer
                self._consumer = None
                self._worker_thread = None
