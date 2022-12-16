from typing import Optional

from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.tui.menu.tui_menu import TUIMenu
from hspylib.modules.cli.vt100.vt_utils import restore_cursor


class TUIMenuView(TUIMenu):
    """TODO"""

    def __init__(
        self,
        parent: TUIMenu,
        display_text: str = None,
        title: Optional[str] = None,
        tooltip: Optional[str] = None):
        super().__init__(parent, title or 'Menu View', tooltip or f"Access the '{title}' view")
        self._content = display_text or f"%ED0%This is a view: {self.title}"

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, text: str) -> None:
        self._content = text

    def execute(self, title: str = "Main Menu") -> Optional[TUIMenu]:

        self._render()
        while not (keypress := Keyboard.wait_keystroke()):
            pass

        return self._on_trigger(self) if keypress != Keyboard.VK_ESC else None

    def _render(self) -> None:
        restore_cursor()
        sysout(self.content)
        sysout(self._navbar())
