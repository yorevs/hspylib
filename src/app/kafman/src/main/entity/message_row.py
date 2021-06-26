class MessageRow:
    """TODO"""
    def __init__(
        self,
        timestamp: int = None,
        event_name: str = None,
        message: str = None):

        self.timestamp = timestamp
        self.event_name = event_name
        self.message = message

    def __str__(self):
        return f"{self.timestamp} [{self.event_name}] {self.message}"

    def __repr__(self):
        return str(self)
