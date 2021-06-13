import threading
from typing import List

from confluent_kafka.cimpl import Consumer

from hspylib.core.metaclass.singleton import Singleton


class KafmanConsumer(metaclass=Singleton):
    """TODO"""
    PARTITION_EOF = -191  # KafkaError._PARTITION_EOF

    def __init__(self):
        super().__init__()
        self.topic = None
        self.consumer = None
        self.started = False

    def start(self, settings: dict) -> None:
        """TODO"""
        if not self.consumer:
            self.consumer = Consumer(settings)
            self.started = True

    def stop(self) -> None:
        """TODO"""
        if self.consumer:
            del self.consumer
            self.consumer = None
            self.started = False

    def consume(self, topics: List[str]) -> None:
        """TODO"""
        if self.consumer is not None:
            print(f"Started consuming from: {topics}")
            tr = threading.Thread(target=self._consume, args=(topics,))
            tr.setDaemon(True)
            tr.start()

    def _consume(self, topics: List[str]) -> None:
        """TODO"""
        self.consumer.subscribe(topics)
        interval = 0.5
        try:
            while self.started:
                msg = self.consumer.poll(interval)
                if msg is None:
                    continue
                elif not msg.error():
                    print(f"Received message: {msg.value()}")
                elif msg.error().code() == self.PARTITION_EOF:
                    print(f"End of partition reached {msg.topic()}/{msg.partition()}")
                else:
                    print(f"Error occurred: {msg.error().str()}")
        except KeyboardInterrupt:
            print("Keyboard interrupted")
        finally:
            if self.consumer:
                self.consumer.close()

