from typing import Callable, List

from hspylib.core.preconditions import check_not_none
from hspylib.modules.cli.tui.menu.tui_menu_item import TUIMenuItem


class TUIMenuFactory:

    class TUIMenuBuilder:

        def __init__(self, parent: TUIMenuItem):
            check_not_none(parent)
            self._main_meni: TUIMenuItem = parent
            self._options: List[TUIMenuItem] = []

        def with_option(self, title: str) -> 'TUIMenuFactory.TUIMenuBuilder':
            self._options.append(TUIMenuItem(self._parent, title))
            return self

        def on_trigger(self, trigger_cb: Callable) -> 'TUIMenuFactory.TUIMenuBuilder':
            return self

    @classmethod
    def create_menu(cls, parent: TUIMenuItem, title: str) -> 'TUIMenuBuilder':
        return cls.TUIMenuBuilder(parent)

