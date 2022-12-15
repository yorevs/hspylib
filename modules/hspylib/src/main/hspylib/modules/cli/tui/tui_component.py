from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

from hspylib.modules.cli.keyboard import Keyboard

ITEM_TYPE = TypeVar("ITEM_TYPE")


class TUIComponent(Generic[ITEM_TYPE], ABC):
    def __init__(self):
        pass

    @abstractmethod
    def render(self) -> None:
        """TODO"""

    @abstractmethod
    def execute(self) -> Optional[ITEM_TYPE | List[ITEM_TYPE]]:
        """TODO"""

    @abstractmethod
    def navbar(self) -> str:
        """TODO"""

    @abstractmethod
    def _handle_keypress(self) -> Keyboard:
        """TODO"""
