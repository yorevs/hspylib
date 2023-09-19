from typing import Callable, Optional

from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.tui.menu.tui_menu import ON_TRIGGER_CB, TUIMenu
from hspylib.modules.cli.tui.menu.tui_menu_utils import TUIMenuUtils
from hspylib.modules.cli.vt100.vt_utils import clear_screen
from hspylib.modules.eventbus import eventbus


class TUIMenuView(TUIMenu):
    """TODO"""

    def __init__(
        self,
        parent: TUIMenu,
        title: Optional[str] = None,
        tooltip: Optional[str] = None,
        display_text: Optional[str] = None):
        super().__init__(parent, title or 'Menu View', tooltip or f"Access the '{title}' view")
        self._on_render: ON_TRIGGER_CB = self._display_content
        self._content: str = display_text or f"%ED0%This is a view: {self.title}"

    def on_render(self, on_render: str | ON_TRIGGER_CB) -> None:
        if isinstance(on_render, str):
            self._content = on_render
            self._on_render = self._display_content
        elif isinstance(on_render, Callable):
            self._on_render = on_render
            self._content = f"%ED0%This is a view: {self.title}"

    def execute(self) -> Optional[TUIMenu]:
        self._render()

        return self._on_trigger(self)

    def _render(self) -> None:
        clear_screen()
        eventbus.emit("tui-menu-ui", "render-app-title")
        self._on_render()
        sysout(self._navbar())

    def _display_content(self) -> None:
        sysout(self._content)
        TUIMenuUtils.wait_keystroke()
