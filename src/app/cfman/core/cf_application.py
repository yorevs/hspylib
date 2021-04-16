import re
from typing import List


class Application:

    @classmethod
    def of(cls, app_line: str):
        parts = re.split(r' {2,}', app_line)
        assert len(parts) >= 6, f"Invalid application line: {app_line}"
        return Application(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5].split(', '))

    def __init__(
            self,
            name: str,
            state: str,
            instances: str,
            memory: str,
            disk: str,
            urls: List[str]):
        self.name = name
        self.state = state
        self.instances = instances
        self.memory = memory
        self.disk = disk
        self.urls = urls

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return str(self)
