import threading
from typing import List

from PyQt5.QtCore import pyqtSignal, QObject
from confluent_kafka.cimpl import Consumer
from confluent_kafka.error import ConsumeError

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import syserr
from kafman.src.main.core.constants import PARTITION_EOF


class KafkaConsumer(QObject):
    """TODO"""

    messageConsumed = pyqtSignal(str, str)

    def __init__(self, poll_interval: float = 0.5):
        super().__init__()
        self.started = False
        self.poll_interval = poll_interval
        self.topic = None
        self.consumer = None
        self.tr = None

    def start(self, settings: dict) -> None:
        """TODO"""
        if self.consumer is None:
            self.consumer = Consumer(settings)
            self.started = True

    def stop(self) -> None:
        """TODO"""
        if self.consumer is not None:
            self.started = False

    def consume(self, topics: List[str]) -> None:
        """TODO"""
        if self.started:
            self.tr = threading.Thread(target=self._consume, args=(topics,))
            self.tr.name = 'kafka-consumer'
            self.tr.setDaemon(True)
            self.tr.start()

    def _consume(self, topics: List[str]) -> None:
        """TODO"""
        try:
            self.consumer.subscribe(topics)
            while self.started and self.consumer is not None:
                message = self.consumer.poll(self.poll_interval)
                if message is None:
                    continue
                elif not message.error():
                    msg = message.value().decode(Charset.UTF_8.value)
                    self.messageConsumed.emit(message.topic(), msg)
                elif message.error().code() == PARTITION_EOF:
                    syserr(f"End of partition reached {message.topic()}/{message.partition()}")
                else:
                    syserr(f"Error occurred: {message.error().str()}")
        except KeyboardInterrupt:
            syserr("Keyboard interrupted")
        except ConsumeError as err:
            syserr(f"An error occurred: {str(err)}")
        finally:
            if self.consumer:
                self.consumer.close()
                del self.consumer
                self.consumer = None
                self.tr = None
