from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List, Any

from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_tools import ensure_endswith, elide_text
from hspylib.modules.cli.icons.font_awesome.awesome import Awesome
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.tui.tui_preferences import TUIPreferences

ITEM_TYPE = TypeVar("ITEM_TYPE")


class TUIComponent(Generic[ITEM_TYPE], ABC):

    @staticmethod
    def _draw_line(line_fmt: str, max_columns: int, *args: Any) -> None:
        """TODO"""
        sysout(ensure_endswith(elide_text(line_fmt.format(*args), max_columns), "%NC%"))

    def __init__(self):
        self.prefs = TUIPreferences()
        self.done = None
        self.require_render = True

    @abstractmethod
    def execute(self, title: str) -> Optional[ITEM_TYPE | List[ITEM_TYPE]]:
        """TODO"""

    def _draw_line_color(self, is_selected: bool) -> Awesome:
        """TODO"""
        if is_selected:
            selector = self.prefs.selected
            sysout(self.prefs.sel_bg_color.code, end="")
            sysout(self.prefs.highlight_color.code, end="")
        else:
            selector = self.prefs.unselected
            sysout(self.prefs.text_color.code, end="")

        return selector

    @abstractmethod
    def _render(self) -> None:
        """TODO"""

    @abstractmethod
    def _navbar(self) -> str:
        """TODO"""

    @abstractmethod
    def _handle_keypress(self) -> Keyboard:
        """TODO"""
