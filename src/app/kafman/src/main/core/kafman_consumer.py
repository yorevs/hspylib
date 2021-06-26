import threading
from typing import List

from PyQt5.QtCore import pyqtSignal, QObject
from confluent_kafka.cimpl import Consumer

from hspylib.core.enums.charset import Charset
from kafman.src.main.core.constants import POLLING_INTERVAL, PARTITION_EOF


class KafmanConsumer(QObject):
    """TODO"""

    messageConsumed = pyqtSignal(str, str)


    def __init__(self):
        super().__init__()
        self.topic = None
        self.consumer = None
        self.started = False

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
                    self.messageConsumed.emit(message.topic(), msg)
                elif message.error().code() == PARTITION_EOF:
                    print(f"End of partition reached {message.topic()}/{message.partition()}")
                else:
                    print(f"Error occurred: {message.error().str()}")
        except KeyboardInterrupt:
            print("Keyboard interrupted")
        finally:
            if self.consumer:
                self.consumer.close()
