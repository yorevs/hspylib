
from typing import List, Optional

from hspylib.modules.cli.tui.menu.tui_menu import TUIMenu, ON_TRIGGER_CB
from hspylib.modules.cli.tui.tui_component import T
from hspylib.modules.cli.vt100.vt_utils import restore_cursor


class TUIMenuAction(TUIMenu):
    """TODO"""

    def execute(self, title: str) -> Optional[T | List[T]]:
        ret_menu = self._on_trigger(self._parent)
        return ret_menu if ret_menu else self._default_trigger_cb(self)

    def _render(self) -> None:
        restore_cursor()

    def __init__(
        self,
        parent: TUIMenu,
        title: Optional[str] = None,
        tooltip: Optional[str] = None,
        on_trigger: ON_TRIGGER_CB = None):

        super().__init__(parent, title, tooltip)
        self._parent = parent
        self._on_trigger = on_trigger or super()._default_trigger_cb

    def on_trigger(self, cb_on_trigger: ON_TRIGGER_CB) -> None:
        """TODO"""
        self._on_trigger = cb_on_trigger
