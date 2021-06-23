import threading
from typing import List

from confluent_kafka.cimpl import Consumer

from hspylib.core.enums.charset import Charset
from hspylib.core.metaclass.singleton import Singleton
from hspylib.modules.eventbus.eventbus import EventBus
from kafman.src.main.core.constants import CONSUMER_BUS, MSG_CONS_EVT, POLLING_INTERVAL, PARTITION_EOF


class KafmanConsumer(metaclass=Singleton):
    """TODO"""

    def __init__(self):
        super().__init__()
        self.topic = None
        self.consumer = None
        self.started = False
        self.bus = EventBus.get(CONSUMER_BUS)

    def start(self, settings: dict) -> None:
        """TODO"""
        if self.consumer is None:
            self.consumer = Consumer(settings)
            self.started = True

    def stop(self) -> None:
        """TODO"""
        if self.consumer is not None:
            del self.consumer
            self.consumer = None
            self.started = False

    def consume(self, topics: List[str]) -> None:
        """TODO"""
        if self.started:
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
                elif message.error().code() == PARTITION_EOF:
                    print(f"End of partition reached {message.topic()}/{message.partition()}")
                else:
                    print(f"Error occurred: {message.error().str()}")
        except KeyboardInterrupt:
            print("Keyboard interrupted")
        finally:
            if self.consumer:
                self.consumer.close()
