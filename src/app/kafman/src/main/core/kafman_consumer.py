from typing import List

from confluent_kafka.cimpl import Consumer

from hspylib.core.metaclass.singleton import Singleton


class KafmanConsumer(metaclass=Singleton):
    """TODO"""

    def __init__(self):
        super().__init__()
        self.topic = None
        self.consumer = None

    def start(self, settings: dict):
        if not self.consumer:
            self.consumer = Consumer(settings)

    def stop(self):
        if self.consumer:
            del self.consumer
            self.consumer = None
