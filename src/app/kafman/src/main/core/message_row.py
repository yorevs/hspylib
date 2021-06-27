from typing import List


class MessageRow:
    """TODO"""

    @staticmethod
    def headers() -> List[str]:
        return ['Timestamp', 'Topic', 'Message']

    def __init__(
        self,
        timestamp: int = None,
        topic: str = None,
        message: str = None):

        self.timestamp = timestamp
        self.topic = topic
        self.message = message

    def __str__(self):
        return f"{self.timestamp} [{self.topic}] {self.message}"

    def __repr__(self):
        return str(self)
