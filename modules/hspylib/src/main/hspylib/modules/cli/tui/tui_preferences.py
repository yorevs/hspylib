import os

from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.dict_tools import get_or_default_by_key
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.cli.icons.font_awesome.nav_icons import Awesome, NavIcons
from hspylib.modules.cli.vt100.vt_color import VtColor


class TUIPreferences(metaclass=Singleton):
    """TODO"""

    INSTANCE = None

    def __init__(self, **kwargs):
        # fmt: off
        self._max_rows: int             = \
            get_or_default_by_key(kwargs, 'max_rows', 15)
        self._items_per_line: int       = \
            get_or_default_by_key(kwargs, 'items_per_line', 5)
        self._title_color: VtColor      = \
            get_or_default_by_key(kwargs, 'title_color', VtColor.ORANGE)
        self._title_line_length: int    = \
            get_or_default_by_key(kwargs, 'title_line_length', 30)
        self._text_color: VtColor       = \
            get_or_default_by_key(kwargs, 'text_color', VtColor.NC)
        self._highlight_color: VtColor  = \
            get_or_default_by_key(kwargs, 'highlight_color', VtColor.CYAN)
        self._navbar_color: VtColor     = \
            get_or_default_by_key(kwargs, 'navbar_color', VtColor.YELLOW)
        self._tooltip_color: VtColor    = \
            get_or_default_by_key(kwargs, 'tooltip_color', VtColor.GREEN)
        self._breadcrumb_color: VtColor = \
            get_or_default_by_key(kwargs, 'breadcrumb_color', VtColor.compose(VtColor.BG_BLUE, VtColor.WHITE))
        self._sel_bg_color: VtColor     = \
            get_or_default_by_key(kwargs, 'sel_bg_color', VtColor.BG_BLUE)
        self._selected: Awesome         = \
            get_or_default_by_key(kwargs, 'selected', NavIcons.POINTER)
        self._unselected: Awesome       = \
            get_or_default_by_key(kwargs, 'unselected', Awesome.no_icon())
        self._marked: Awesome           = \
            get_or_default_by_key(kwargs, 'marked', FormIcons.MARKED)
        self._unmarked: Awesome         = \
            get_or_default_by_key(kwargs, 'unmarked', FormIcons.UNMARKED)
        # fmt: on

    def __str__(self):
        # fmt: off
        return (
            f"Terminal UI Preferences{os.linesep}"
            f"{'-=' * 20}{os.linesep}"
            + os.linesep.join([f"|-{p[1:]:<16}: {getattr(self, p)}" for p in vars(self)])
            + f"{os.linesep}{'-=' * 20}{os.linesep}"
        )
        # fmt: on

    def __repr__(self):
        return str(self)

    @property
    def max_rows(self) -> int:
        return max(5, self._max_rows)

    @property
    def items_per_line(self) -> int:
        return max(3, self._items_per_line)

    @property
    def title_color(self) -> VtColor:
        return self._title_color

    @property
    def title_line_length(self) -> int:
        return self._title_line_length

    @property
    def text_color(self) -> VtColor:
        return self._text_color

    @property
    def highlight_color(self) -> VtColor:
        return self._highlight_color

    @property
    def navbar_color(self) -> VtColor:
        return self._navbar_color

    @property
    def tooltip_color(self) -> VtColor:
        return self._tooltip_color

    @property
    def breadcrumb_color(self) -> VtColor:
        return self._breadcrumb_color

    @property
    def sel_bg_color(self) -> VtColor:
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
