from typing import List

from confluent_kafka.cimpl import Producer

from hspylib.core.metaclass.singleton import Singleton


class KafmanProducer(metaclass=Singleton):
    """TODO"""

    def __init__(self, settings: dict, topic: List[str]):
        super().__init__()
        self.settings = settings
        self.topic = topic
        self.producer = Producer(settings)
