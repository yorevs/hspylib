from typing import Any, Callable

from hspylib.modules.cli.icons.font_awesome.awesome import Awesome
from hspylib.modules.cli.menu.extra.mdashboard.dashboard_item import DashboardItem


class DashboardItemBuilder:
    def __init__(self, parent: Any):
        self.parent = parent
        self.item = DashboardItem()

    def icon(self, icon: Awesome) -> Any:
        self.item.icon = icon
        return self

    def tooltip(self, tooltip: str) -> Any:
        self.item.tooltip = tooltip
        return self

    def action(self, action: Callable) -> Any:
        self.item.action = action
        return self

    def build(self) -> Any:
        self.parent.items.append(self.item)
        return self.parent
