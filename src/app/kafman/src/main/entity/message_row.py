class MessageRow:
    def __init__(self, event_name: str = None, timestamp: int = None, message: str = None):
        self.event_name = event_name
        self.timestamp = timestamp
        self.message = message
