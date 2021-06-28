import threading
from typing import List, Any

from PyQt5.QtCore import pyqtSignal, QObject
from confluent_kafka.cimpl import Producer, KafkaError

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import syserr
from kafman.src.main.core.constants import POLLING_INTERVAL, FLUSH_WAIT_TIME


class KafkaProducer(QObject):
    """TODO"""

    messageProduced = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.topic = None
        self.producer = None
        self.started = False
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
                self.producer.poll(POLLING_INTERVAL)
        except KeyboardInterrupt:
            syserr("Keyboard interrupted")
        finally:
            self.producer.flush(FLUSH_WAIT_TIME)

    def _cb_message_produced(self, error: KafkaError, message: Any) -> None:
        """TODO"""
        msg = message.value().decode(Charset.UTF_8.value)
        if error is not None:
            syserr(f"Failed to deliver message: {msg}: {error.str()}")
        else:
            self.messageProduced.emit(message.topic(), msg)
