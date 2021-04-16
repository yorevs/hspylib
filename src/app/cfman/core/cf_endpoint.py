from typing import Tuple


class Endpoint:

    def __init__(self, attrs: Tuple[str]):
        self.alias = attrs[0]
        self.host = attrs[1]
        self.protected = attrs[2]

    def __str__(self) -> str:
        return f'{self.alias}  {self.host}'

    def __repr__(self):
        return str(self)
