from typing import List


class MessageRow:
    """TODO"""

    @staticmethod
    def headers() -> List[str]:
        return ['Timestamp', 'Topic', 'Partition', 'Offset', 'Value']

    def __init__(
        self,
        timestamp: int = None,
        topic: str = None,
        partition: int = None,
        offset: int = None,
        value: str = None):

        self.timestamp = timestamp
        self.topic = topic
        self.partition = partition
        self.offset = offset
        self.value = value

    def __str__(self):
        return f"{self.timestamp} topic={self.topic} partition={self.partition} offset={self.offset} value={self.value}"

    def __repr__(self):
        return str(self)
