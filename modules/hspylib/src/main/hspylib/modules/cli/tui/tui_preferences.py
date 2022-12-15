import os

from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.dict_tools import get_or_default_by_key
from hspylib.modules.cli.icons.font_awesome.nav_icons import NavIcons
from hspylib.modules.cli.vt100.vt_colors import VtColors


class TUIPreferences(metaclass=Singleton):
    """TODO"""

    def __init__(self, **kwargs):
        self._max_rows: int = get_or_default_by_key(kwargs, 'max_rows', 15)
        self._title_color: VtColors = get_or_default_by_key(kwargs, 'title_color', VtColors.ORANGE)
        self._highlight_color: VtColors = get_or_default_by_key(kwargs, 'highlight_color', VtColors.BLUE)
        self._navbar_color: VtColors = get_or_default_by_key(kwargs, 'navbar_color', VtColors.YELLOW)
        self._sel_bg_color: VtColors = get_or_default_by_key(kwargs, 'navbar_color', VtColors.YELLOW)
        self._selector: NavIcons = get_or_default_by_key(kwargs, 'selector', NavIcons.SELECTOR)

    def __str__(self):
        return \
        f"Terminal UI Preferences{os.linesep}" \
        f"{'-=' * 20}{os.linesep}" \
        + os.linesep.join([f"|-{p[1:]:<16}: {getattr(self, p)}" for p in vars(self)]) \
        + f"{os.linesep}{'-=' * 20}{os.linesep}"

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    pref = TUIPreferences()
    print(str(pref))
