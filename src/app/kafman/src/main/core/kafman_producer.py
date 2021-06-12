from typing import List

from confluent_kafka.cimpl import Producer

from hspylib.core.metaclass.singleton import Singleton


class KafmanProducer(metaclass=Singleton):
    """TODO"""

    @staticmethod
    def message_produced(err, msg) -> None:
        """TODO"""
        if err is not None:
            print(f"Failed to deliver message: {msg.value()}: {err.str()}")
        else:
            print(f"Message produced: {msg.value()}")

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
        if not self.producer:
            self.producer = Producer(settings)
            self.started = True

    def stop(self) -> None:
        """TODO"""
        if self.producer:
            self.purge()
            self.flush()
            del self.producer
            self.producer = None
            self.started = False

    def produce(self, topics: List[str], messages: List[str]) -> None:
        """TODO"""
        if self.producer is not None:
            try:
                for topic in topics:
                    for msg in messages:
                        self.producer.produce(topic, msg, callback=self.message_produced)
                        self.producer.poll(0.5)
            except KeyboardInterrupt:
                pass
            finally:
                self.producer.flush(30)
