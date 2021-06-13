import threading
from typing import List

from confluent_kafka.cimpl import Producer, Message, KafkaError

from hspylib.core.enums.charset import Charset
from hspylib.core.metaclass.singleton import Singleton
from hspylib.modules.eventbus.eventbus import EventBus
from hspylib.modules.qt.promotions.hconsole import HConsole
from kafman.src.main.core.constants import PRODUCER_BUS, MSG_PROD_EVT, POLLING_INTERVAL


class KafmanProducer(metaclass=Singleton):
    """TODO"""

    def __init__(self):
        super().__init__()
        self.topic = None
        self.producer = None
        self.started = False
        self.bus = EventBus.get(PRODUCER_BUS)
        self.console_bus = EventBus.get(HConsole.CONSOLE_BUS)

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
            self._console_print("Keyboard interrupted")
        finally:
            self.producer.flush(30)

    def _message_produced(self, error: KafkaError, message: Message) -> None:
        """TODO"""
        topic = message.topic()
        msg = message.value().decode(Charset.UTF_8.value)
        if error is not None:
            self._console_print(f"Failed to deliver message: {msg}: {error.str()}")
        else:
            self.bus.emit(MSG_PROD_EVT, message=msg, topic=topic)

    def _console_print(self, text: str) -> None:
        """TODO"""
        self.console_bus.emit(HConsole.TEXT_DISPATCHED_EVT, text=text)
