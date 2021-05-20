from typing import Any

from hspylib.modules.cli.menu.extra.mdashboard.dashboard_item_builder import DashboardItemBuilder


class DashboardBuilder:
    def __init__(self):
        self.items = []

    def item(self) -> Any:
        return DashboardItemBuilder(self)

    def build(self) -> list:
        return self.items
