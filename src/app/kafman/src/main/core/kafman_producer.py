from typing import List

from confluent_kafka.cimpl import Producer

from hspylib.core.metaclass.singleton import Singleton


class KafmanProducer(metaclass=Singleton):
    """TODO"""

    def __init__(self):
        super().__init__()
        self.topic = None
        self.producer = None

    def flush(self, timeout: int = 0):
        if self.producer:
            self.producer.flush(timeout=timeout)

    def purge(self):
        if self.producer:
            self.producer.purge()

    def start(self, settings: dict):
        if not self.producer:
            self.producer = Producer(settings)

    def stop(self):
        if self.producer:
            self.purge()
            self.flush()
            del self.producer
            self.producer = None
