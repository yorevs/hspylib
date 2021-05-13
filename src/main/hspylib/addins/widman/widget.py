from abc import ABC, abstractmethod
from typing import Tuple, final


class Widget(ABC):
    USAGE = """
    HSPyLib Widget: {} v{}
    
    Report system memory usage.
    """

    def __init__(
            self,
            name: str,
            version: Tuple[int, int, int],
            info: str):

        self._name = name
        self._info = info
        self._version = version

    @abstractmethod
    def execute(self):
        """Execute the widget main flow"""

    @abstractmethod
    def cleanup(self):
        """Execute the widget cleanup"""

    @final
    def name(self) -> str:
        """Return the name about the widget"""
        return self._name

    @final
    def info(self) -> str:
        """Return information about the widget"""
        return self._info

    @final
    def version(self) -> Tuple[int, int, int]:
        """Return the version of the widget"""
        return self._version

    @final
    def usage(self) -> str:
        """Return a usage message about the widget"""
        return self.USAGE
