import threading
from typing import List, Any

from PyQt5.QtCore import pyqtSignal, QObject
from confluent_kafka.cimpl import Producer, KafkaError

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import syserr


class KafkaProducer(QObject):
    """TODO"""

    messageProduced = pyqtSignal(str, str)

    def __init__(self, poll_interval: float = 0.5, flush_timeout: int = 30):
        super().__init__()
        self.started = False
        self.poll_interval = poll_interval
        self.flush_timeout = flush_timeout
        self.topic = None
        self.producer = None
        self.tr = None

    def flush(self, timeout: int = 0) -> None:
        """TODO"""
        if self.producer:
            self.producer.flush(timeout=timeout)

    def purge(self) -> None:
        """TODO"""
        if self.producer:
            self.producer.purge()

    def start(self, settings: dict) -> None:
        """TODO"""
        if self.producer is None:
            self.producer = Producer(settings)
            self.started = True

    def stop(self) -> None:
        """TODO"""
        if self.producer is not None:
            self.purge()
            self.flush()
            self.started = False
            del self.producer
            self.producer = None
            self.tr = None

    def produce(self, topics: List[str], messages: List[str]) -> None:
        """TODO"""
        if self.started and self.producer is not None:
            self.tr = threading.Thread(target=self._produce, args=(topics,messages,))
            self.tr.name = 'kafka-producer'
            self.tr.setDaemon(True)
            self.tr.start()
            self.tr.join()

    def _produce(self, topics: List[str], messages: List[str]):
        """TODO"""
        try:
            for topic in topics:
                for msg in messages:
                    if msg:
                        self.producer.produce(topic, msg, callback=self._cb_message_produced)
                self.producer.poll(self.poll_interval)
        except KeyboardInterrupt:
            syserr("Keyboard interrupted")
        finally:
            self.producer.flush(self.flush_timeout)

    def _cb_message_produced(self, error: KafkaError, message: Any) -> None:
        """TODO"""
        msg = message.value().decode(Charset.UTF_8.value)
        if error is not None:
            syserr(f"Failed to deliver message: {msg}: {error.str()}")
        else:
            self.messageProduced.emit(message.topic(), msg)
