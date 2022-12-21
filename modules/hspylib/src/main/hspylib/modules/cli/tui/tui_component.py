from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List, Any

from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_tools import ensure_endswith, elide_text
from hspylib.modules.cli.icons.font_awesome.awesome import Awesome
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.tui.tui_preferences import TUIPreferences

T = TypeVar("T")


class TUIComponent(Generic[T], ABC):

    @staticmethod
    def _draw_line(line_fmt: str, max_columns: int, *args: Any) -> None:
        """TODO"""
        sysout(ensure_endswith(elide_text(line_fmt.format(*args), max_columns), "%NC%"))

    def __init__(self, title: str = None):
        self.prefs: TUIPreferences = TUIPreferences.INSTANCE or TUIPreferences()
        self._done: bool = False
        self._re_render: bool = True
        self._title: str = title

    @property
    def title(self) -> str:
        return self._title

    @abstractmethod
    def execute(self) -> Optional[T | List[T]]:
        """TODO"""

    def _draw_line_color(self, is_selected: bool = False, set_bg_color: bool = True) -> Awesome:
        """TODO"""
        if is_selected:
            selector = self.prefs.selected
            if set_bg_color:
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
    def _navbar(self, *args) -> str:
        """TODO"""

    @abstractmethod
    def _handle_keypress(self) -> Keyboard:
        """TODO"""
