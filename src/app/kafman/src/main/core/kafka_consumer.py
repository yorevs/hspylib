import threading
from typing import List

from PyQt5.QtCore import pyqtSignal, QObject
from confluent_kafka.cimpl import Consumer

from hspylib.core.tools.commons import syserr

# Example at https://docs.confluent.io/platform/current/tutorials/examples/clients/docs/python.html
class KafkaConsumer(QObject):
    """TODO"""

    messageConsumed = pyqtSignal(str, int, int, bytes)

    def __init__(self, poll_interval: float = 0.5):
        super().__init__()
        self._started = False
        self._poll_interval = poll_interval
        self._consumer = None
        self._worker_thread = None

    def start(self, settings: dict) -> None:
        """TODO"""
        if self._consumer is None:
            self._consumer = Consumer(settings)
            self._started = True

    def stop(self) -> None:
        """TODO"""
        if self._consumer is not None:
            self._started = False

    def consume(self, topics: List[str]) -> None:
        """TODO"""
        if self._started:
            self._worker_thread = threading.Thread(target=self._consume, args=(topics,))
            self._worker_thread.name = 'kafka-consumer'
            self._worker_thread.setDaemon(True)
            self._worker_thread.start()

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
