#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: clitt.core.tui.menu
      @file: tui_menu_factory.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import List, TypeVar, Union

from hspylib.core.preconditions import check_not_none

from clitt.core.tui.menu.tui_menu import TUIMenu
from clitt.core.tui.menu.tui_menu_action import ON_TRIGGER_CB, TUIMenuAction
from clitt.core.tui.menu.tui_menu_item import TUIMenuItem
from clitt.core.tui.menu.tui_menu_view import TUIMenuView

AnyBuilder = TypeVar(
    'AnyBuilder',
    bound=Union[
        'TUIMenuFactory.TUIMenuBuilder',
        'TUIMenuFactory.TUIMenuItemBuilder',
        'TUIMenuFactory.TUIMenuViewBuilder',
    ]
)


class TUIMenuFactory:

    _main_menu = None

    class TUIMenuBuilder:

        def __init__(
            self,
            parent: 'TUIMenuFactory',
            main_menu: TUIMenuItem):
            check_not_none((parent, main_menu))
            self._parent = parent
            self._main_menu: TUIMenuItem = main_menu

        def with_item(self, title: str, tooltip: str | None = None) -> 'TUIMenuFactory.TUIMenuItemBuilder':
            return TUIMenuFactory.TUIMenuItemBuilder(self, self._main_menu, title, tooltip)

        def with_action(self, title: str, tooltip: str | None = None) -> 'TUIMenuFactory.TUIMenuActionBuilder':
            return TUIMenuFactory.TUIMenuActionBuilder(self, self._main_menu, title, tooltip)

        def with_view(self, title: str, tooltip: str | None = None) -> 'TUIMenuFactory.TUIMenuViewBuilder':
            return TUIMenuFactory.TUIMenuViewBuilder(self, self._main_menu, title, tooltip)

        def then(self) -> 'TUIMenuFactory':
            return self._parent

    class TUIMenuItemBuilder:

        def __init__(
            self,
            parent: AnyBuilder,
            parent_item: TUIMenuItem,
            title: str = None,
            tooltip: str | None = None):
            check_not_none((parent, parent_item))
            self._parent = parent
            self._menu_item = TUIMenuItem(parent_item, title, tooltip)
            self._items: List[TUIMenu] = []
            parent_item.add_items(self._menu_item)

        def with_item(self, title: str, tooltip: str | None = None) -> 'TUIMenuFactory.TUIMenuItemBuilder':
            return TUIMenuFactory.TUIMenuItemBuilder(self, self._menu_item, title, tooltip)

        def with_action(self, title: str, tooltip: str | None = None) -> 'TUIMenuFactory.TUIMenuActionBuilder':
            return TUIMenuFactory.TUIMenuActionBuilder(self, self._menu_item, title, tooltip)

        def with_view(self, title: str, tooltip: str | None = None) -> 'TUIMenuFactory.TUIMenuViewBuilder':
            return TUIMenuFactory.TUIMenuViewBuilder(self, self._menu_item, title, tooltip)

        def then(self) -> AnyBuilder:
            return self._parent

    class TUIMenuViewBuilder:

        def __init__(
            self,
            parent: AnyBuilder,
            parent_item: TUIMenuItem,
            title: str = None,
            tooltip: str | None = None):
            check_not_none((parent, parent_item))
            self._parent = parent
            self._menu_view = TUIMenuView(parent_item, title, tooltip)
            parent_item.add_items(self._menu_view)

        def on_render(self, on_render: str | ON_TRIGGER_CB) -> 'TUIMenuFactory.TUIMenuItemBuilder':
            self._menu_view.on_render(on_render)
            return self._parent

    class TUIMenuActionBuilder:

        def __init__(
            self,
            parent: AnyBuilder,
            parent_item: TUIMenuItem,
            title: str = None,
            tooltip: str | None = None):
            check_not_none((parent, parent_item))
            self._parent = parent
            self._menu_action = TUIMenuAction(parent_item, title, tooltip)
            self._parent_item = parent_item
            parent_item.add_items(self._menu_action)

        def on_trigger(self, action: ON_TRIGGER_CB) -> 'TUIMenuFactory.TUIMenuItemBuilder':
            check_not_none(action)
            self._menu_action.on_trigger(action)
            return self._parent

    @classmethod
    def create_main_menu(
        cls,
        title: str = None,
        tooltip: str | None = None) -> 'TUIMenuBuilder':
        cls._main_menu: TUIMenuItem = TUIMenuItem(title=title, tooltip=tooltip)
        factory = TUIMenuFactory()

        return cls.TUIMenuBuilder(factory, cls._main_menu)

    def build(self) -> TUIMenuItem:
        return self._main_menu
