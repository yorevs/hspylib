class Event:
    """TODO"""

    def __init__(self, _name_: str, **kwargs):
        self.name = _name_
        self.kwargs = kwargs

    def __str__(self):
        return f"{self.name}: {str(self.kwargs)}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other: 'Event'):
        return self.name == other.name and self.kwargs == other.kwargs

    def __getitem__(self, item: str):
        return self.kwargs[item]
