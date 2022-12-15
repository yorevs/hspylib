import os

from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.dict_tools import get_or_default_by_key
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.cli.icons.font_awesome.nav_icons import Awesome, NavIcons
from hspylib.modules.cli.vt100.vt_colors import VtColors


class TUIPreferences(metaclass=Singleton):
    """TODO"""

    INSTANCE = None

    def __init__(self, **kwargs):
        self._max_rows: int = get_or_default_by_key(kwargs, 'max_rows', 15)
        self._title_color: VtColors = get_or_default_by_key(kwargs, 'title_color', VtColors.ORANGE)
        self._text_color: VtColors = get_or_default_by_key(kwargs, 'text_color', VtColors.NC)
        self._highlight_color: VtColors = get_or_default_by_key(kwargs, 'highlight_color', VtColors.CYAN)
        self._navbar_color: VtColors = get_or_default_by_key(kwargs, 'navbar_color', VtColors.YELLOW)
        self._sel_bg_color: VtColors = get_or_default_by_key(kwargs, 'navbar_color', VtColors.BG_BLUE)
        self._selected: Awesome = get_or_default_by_key(kwargs, 'selected', NavIcons.POINTER)
        self._unselected: Awesome = get_or_default_by_key(kwargs, 'unselected', Awesome.no_icon())
        self._marked: Awesome = get_or_default_by_key(kwargs, 'marked', FormIcons.MARKED)
        self._unmarked: Awesome = get_or_default_by_key(kwargs, 'unmarked', FormIcons.UNMARKED)

    def __str__(self):
        return \
        f"Terminal UI Preferences{os.linesep}" \
        f"{'-=' * 20}{os.linesep}" \
        + os.linesep.join([f"|-{p[1:]:<16}: {getattr(self, p)}" for p in vars(self)]) \
        + f"{os.linesep}{'-=' * 20}{os.linesep}"

    def __repr__(self):
        return str(self)

    @property
    def max_rows(self) -> int:
        return max(5, self._max_rows)

    @property
    def title_color(self) -> VtColors:
        return self._title_color

    @property
    def text_color(self) -> VtColors:
        return self._text_color

    @property
    def highlight_color(self) -> VtColors:
        return self._highlight_color

    @property
    def navbar_color(self) -> VtColors:
        return self._navbar_color

    @property
    def sel_bg_color(self) -> VtColors:
        return self._sel_bg_color

    @property
    def selected(self) -> Awesome:
        return self._selected

    @property
    def unselected(self) -> Awesome:
        return self._unselected

    @property
    def marked(self) -> Awesome:
        return self._marked

    @property
    def unmarked(self) -> Awesome:
        return self._unmarked
