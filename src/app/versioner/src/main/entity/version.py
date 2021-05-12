import re
from typing import Any

from versioner.src.main.enum.extension import Extension


class Version:

    @classmethod
    def of(cls, version_str: str) -> Any:
        parts = list(map(str.strip, re.split(r'[.-]', version_str)))
        return Version(
            int(parts[0]),
            int(parts[1]),
            int(parts[2]),
            Extension.value_of(parts[3]))

    def __init__(self, major: int, minor: int, patch: int, state: Extension):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.state = state

    def __str__(self):
        release = '-' + str(self.state) if self.state else ''
        return f"{self.major:d}.{self.minor:d}.{self.patch:d}{release:s}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return \
            self.major == other.major \
            and self.minor == other.minor \
            and self.patch == other.patch \
            and self.state == other.state
