from typing import List

from confluent_kafka.cimpl import Consumer

from hspylib.core.metaclass.singleton import Singleton


class KafmanConsumer(metaclass=Singleton):
    """TODO"""

    def __init__(self, settings: dict, topic: List[str]):
        super().__init__()
        self.settings = settings
        self.topic = topic
        self.consumer = Consumer(settings)
