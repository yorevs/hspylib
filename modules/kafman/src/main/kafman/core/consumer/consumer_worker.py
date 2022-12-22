#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: consumer_worker.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import threading
from time import sleep
from typing import List

from confluent_kafka import DeserializingConsumer
from confluent_kafka.error import ConsumeError, ValueDeserializationError
from hspylib.core.tools.commons import syserr
from PyQt5.QtCore import pyqtSignal, QThread

from kafman.core.schema.kafka_schema import KafkaSchema


class ConsumerWorker(QThread):
    """Confluent Kafka Consumer with Qt.
    Example at https://docs.confluent.io/platform/current/tutorials/examples/clients/docs/python.html
    For all kafka settings: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    Ref:. https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/json_consumer.py
    """

    messageConsumed = pyqtSignal(str, int, int, str)
    messageFailed = pyqtSignal(str)

    def __init__(self, poll_interval: float = 0.5):
        super().__init__()
        self.setObjectName("kafka-consumer")
        self._started = False
        self._poll_interval = poll_interval
        self._consumer = None
        self._worker_thread = None
        self._schema = None
        self.start()

    def start_consumer(self, settings: dict, schema: KafkaSchema) -> None:
        """Start the Kafka consumer agent"""
        if self._consumer is None:
            self._schema = schema
            self._consumer = DeserializingConsumer(settings)
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
            self._worker_thread.daemon = True
            self._worker_thread.start()

    def is_started(self) -> bool:
        """Whether the consumer is started or not"""
        return self._started

    def run(self) -> None:
        while not self.isFinished():
            sleep(self._poll_interval)

    def commit(self, offset: int):
        """TODO"""
        topic_partitions = self._consumer.assignment()
        for tp in topic_partitions:
            tp.offset = offset + 1
            self._consumer.commit(offsets=topic_partitions, asynchronous=False)

    def schema(self) -> KafkaSchema:
        """TODO"""
        return self._schema

    def _consume(self, topics: List[str]) -> None:
        """Consume messages from the selected Kafka topics"""
        try:
            self._consumer.subscribe(topics)
            while self._started and self._consumer is not None:
                try:
                    message = self._consumer.poll(self._poll_interval)
                    if message is None:
                        continue
                    if message.error():
                        self.messageFailed.emit(str(message.error()))
                    else:
                        self.messageConsumed.emit(
                            message.topic(), message.partition(), message.offset(), str(message.value())
                        )
                except (ValueDeserializationError, ConsumeError) as err:
                    self.messageFailed.emit(str(err))
        except KeyboardInterrupt:
            syserr("Keyboard interrupted")
        finally:
            if self._consumer:
                self._consumer.close()
                del self._consumer
                self._consumer = None
                self._worker_thread = None
