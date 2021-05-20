from collections import Callable

from hspylib.modules.cli.icons.font_awesome.awesome import Awesome


class DashboardItem:
    def __init__(
            self,
            icon: Awesome = None,
            tooltip: str = None,
            action: Callable = None):
        self.icon = icon
        self.tooltip = tooltip
        self.action = action
