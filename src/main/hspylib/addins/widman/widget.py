from abc import ABC, abstractmethod
from typing import Tuple, final

from hspylib.modules.cli.icons.font_awesome.awesome import Awesome


class Widget(ABC):
    USAGE = """
    HSPyLib Widget: {} v{}
    
    Report system memory usage.
    """

    def __init__(
            self,
            icon: Awesome,
            name: str,
            version: Tuple[int, int, int],
            tooltip: str):

        self._icon = icon
        self._name = name
        self._tooltip = tooltip
        self._version = version

    @abstractmethod
    def execute(self):
        """Execute the widget main flow"""

    @abstractmethod
    def cleanup(self):
        """Execute the widget cleanup"""

    @final
    def icon(self) -> Awesome:
        return self._icon

    @final
    def name(self) -> str:
        """Return the name about the widget"""
        return self._name

    @final
    def tooltip(self) -> str:
        """Return information about the widget"""
        return self._tooltip

    @final
    def version(self) -> Tuple[int, int, int]:
        """Return the version of the widget"""
        return self._version

    @final
    def usage(self) -> str:
        """Return a usage message about the widget"""
        return self.USAGE
