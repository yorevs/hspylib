import threading
from typing import List

from confluent_kafka.cimpl import Consumer

from hspylib.core.enums.charset import Charset
from hspylib.core.metaclass.singleton import Singleton
from hspylib.modules.eventbus.eventbus import EventBus
from kafman.src.main.core.constants import CONSUMER_BUS, MSG_CONS_EVT, POLLING_INTERVAL


class KafmanConsumer(metaclass=Singleton):
    """TODO"""
    PARTITION_EOF = -191  # KafkaError._PARTITION_EOF

    def __init__(self):
        super().__init__()
        self.topic = None
        self.consumer = None
        self.started = False
        self.bus = EventBus.get(CONSUMER_BUS)

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
        try:
            while self.started:
                message = self.consumer.poll(POLLING_INTERVAL)
                if message is None:
                    continue
                elif not message.error():
                    msg = message.value().decode(Charset.UTF_8.value)
                    self.bus.emit(MSG_CONS_EVT, message=msg, topic=message.topic())
                    print(f"Consumed message: {msg}")
                elif message.error().code() == self.PARTITION_EOF:
                    print(f"End of partition reached {message.topic()}/{message.partition()}")
                else:
                    print(f"Error occurred: {message.error().str()}")
        except KeyboardInterrupt:
            print("Keyboard interrupted")
        finally:
            if self.consumer:
                self.consumer.close()

