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
from time import sleep
from typing import List

from PyQt5.QtCore import pyqtSignal, QThread
from avro.io import AvroTypeException
from confluent_kafka.cimpl import Producer, KafkaError, Message  # pylint: disable=

from hspylib.core.enums.charset import Charset
from hspylib.modules.qt.kafka.avro_schema import AvroSchema

from hspylib.core.tools.commons import syserr


# Example at: # Example at https://docs.confluent.io/platform/current/tutorials/examples/clients/docs/python.html
# For all kafka settings: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
class KafkaProducer(QThread):
    """TODO"""

    plainMessageProduced = pyqtSignal(str, int, int, bytes)
    avroMessageProduced = pyqtSignal(str, int, int, bytes)

    def __init__(self, poll_interval: float = 0.5, flush_timeout: int = 30):
        super().__init__()
        self.setObjectName('kafka-producer')
        self._started = False
        self._poll_interval = poll_interval
        self._flush_timeout = flush_timeout
        self._schema = None
        self._producer = None
        self._worker_thread = None
        self.start()

    def start_producer(self, settings: dict) -> None:
        """Start the producer"""
        if self._producer is None:
            self._producer = Producer(settings)
            self._started = True

    def stop_producer(self) -> None:
        """Stop the producer."""
        if self._producer is not None:
            self._purge()
            self._flush()
            self._started = False
            del self._producer
            self._producer = None
            self._worker_thread = None
            self._schema = None

    def produce(self, topics: List[str], messages: List[str]) -> None:
        """Create a worker thread to produce the messages to the specified topics."""
        if self._started and self._producer is not None:
            self._worker_thread = threading.Thread(target=self._produce, args=(topics, messages,))
            self._worker_thread.name = f"kafka-producer-worker-{hash(self)}"
            self._worker_thread.setDaemon(True)
            self._worker_thread.start()

    def set_schema(self, schema: AvroSchema) -> None:
        self._schema = schema

    def is_started(self) -> bool:
        """Whether the producer is started or not."""
        return self._started

    def run(self) -> None:
        while not self.isFinished():
            sleep(self._poll_interval)

    def _flush(self, timeout: int = 0) -> None:
        """Wait for all messages in the Producer queue to be delivered."""
        if self._producer:
            self._producer.flush(timeout=timeout)

    def _purge(self) -> None:
        """Purge messages currently handled by the producer instance."""
        if self._producer:
            self._producer.purge()

    def _produce(self, topics: List[str], messages: List[str]) -> None:
        """Produce message to topic."""
        try:
            for topic in topics:
                for msg in messages:
                    if msg:
                        if not self._schema:
                            encoded_msg = msg.encode(Charset.CP1250.value)
                            self._producer.produce(topic, encoded_msg, callback=self._cb_plain_message_produced)
                        else:
                            encoded_msg = self._schema.encode(msg)
                            self._producer.produce(topic, encoded_msg, callback=self._cb_avro_message_produced)
                self._producer.poll(self._poll_interval)
        except KeyboardInterrupt:
            syserr("Keyboard interrupted")
        except AvroTypeException as err:
            syserr(str(err))
        finally:
            self._producer.flush(self._flush_timeout)

    def _cb_plain_message_produced(self, err: KafkaError, message: Message) -> None:
        """Delivery report handler called on successful or failed delivery of message"""
        if err is not None:
            syserr(f"Failed to deliver PLAIN message: {err}")
        else:
            self.plainMessageProduced.emit(
                message.topic(), message.partition(), message.offset(), message.value())

    def _cb_avro_message_produced(self, err: KafkaError, message: Message) -> None:
        """Delivery report handler called on successful or failed delivery of an avro schema message"""
        if err is not None:
            syserr(f"Failed to deliver AVRO message: {err}")
        else:
            self.avroMessageProduced.emit(
                message.topic(), message.partition(), message.offset(), self._schema.decode(message.value()))
