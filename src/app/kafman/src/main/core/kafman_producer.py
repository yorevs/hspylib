import threading
from typing import List

from PyQt5.QtCore import pyqtSignal, QObject
from confluent_kafka.cimpl import Producer, Message, KafkaError

from hspylib.core.enums.charset import Charset
from kafman.src.main.core.constants import POLLING_INTERVAL


class KafmanProducer(QObject):
    """TODO"""

    messageProduced = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.topic = None
        self.producer = None
        self.started = False

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
            del self.producer
            self.producer = None
            self.started = False

    def produce(self, topics: List[str], messages: List[str]) -> None:
        """TODO"""
        if self.started:
            tr = threading.Thread(target=self._produce, args=(topics,messages,))
            tr.setDaemon(True)
            tr.start()

    def _produce(self, topics: List[str], messages: List[str]):
        """TODO"""
        try:
            for topic in topics:
                for msg in messages:
                    if msg:
                        self.producer.produce(topic, msg, callback=self._message_produced)
                self.producer.poll(POLLING_INTERVAL)
        except KeyboardInterrupt:
            print("Keyboard interrupted")
        finally:
            self.producer.flush(30)

    def _message_produced(self, error: KafkaError, message: Message) -> None:
        """TODO"""
        msg = message.value().decode(Charset.UTF_8.value)
        if error is not None:
            print(f"Failed to deliver message: {msg}: {error.str()}")
        else:
            self.messageProduced.emit(f"topic={message.topic()} message={msg}")
