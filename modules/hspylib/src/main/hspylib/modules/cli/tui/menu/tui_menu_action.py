
from typing import Optional

from hspylib.modules.cli.tui.menu.tui_menu import ON_TRIGGER_CB, TUIMenu
from hspylib.modules.cli.tui.menu.tui_menu_utils import TUIMenuUtils
from hspylib.modules.cli.vt100.vt_utils import restore_cursor
from hspylib.modules.eventbus import eventbus


class TUIMenuAction(TUIMenu):
    """TODO"""

    def execute(self) -> Optional[TUIMenu]:
        self._render()
        ret_menu = self._on_trigger(self._parent)
        if not ret_menu:
            TUIMenuUtils.wait_keystroke()
        return ret_menu if ret_menu else self._default_trigger_cb(self)

    def _render(self) -> None:
        restore_cursor()
        eventbus.emit("tui-menu-ui", "render-app-title")

    def __init__(
        self,
        parent: TUIMenu,
        title: Optional[str] = None,
        tooltip: Optional[str] = None,
        on_trigger: ON_TRIGGER_CB = None):

        super().__init__(parent, title, tooltip)
        self._parent = parent
        self._on_trigger: ON_TRIGGER_CB = on_trigger or super()._default_trigger_cb

    def on_trigger(self, cb_on_trigger: ON_TRIGGER_CB) -> None:
        """TODO"""
        self._on_trigger = cb_on_trigger
