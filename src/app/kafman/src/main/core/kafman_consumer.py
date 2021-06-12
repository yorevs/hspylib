from typing import List

from confluent_kafka.cimpl import Consumer, KafkaError

from hspylib.core.metaclass.singleton import Singleton


class KafmanConsumer(metaclass=Singleton):
    """TODO"""

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
        if self.consumer:
            self.consumer.subscribe(topics)
            try:
                while self.started:
                    msg = self.consumer.poll(0.1)
                    if msg is None:
                        continue
                    elif not msg.error():
                        print(f"Received message: {msg.value()}")
                    elif msg.error().code() == -191:  # KafkaError._PARTITION_EOF
                        print(f"End of partition reached {msg.topic()}/{msg.partition()}")
                    else:
                        print(f"Error occurred: {msg.error().str()}")

            except KeyboardInterrupt:
                pass

            finally:
                self.consumer.close()

