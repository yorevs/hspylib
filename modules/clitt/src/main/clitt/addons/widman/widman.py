#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.widman
      @file: widman.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.addons.widman.widget import Widget
from clitt.addons.widman.widget_entry import WidgetEntry
from clitt.core.tui.mdashboard.dashboard_item import DashboardItem
from clitt.core.tui.mdashboard.mdashboard import mdashboard
from hspylib.core.exception.exceptions import WidgetExecutionError, WidgetNotFoundError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_state
from hspylib.core.tools.commons import get_path
from hspylib.core.tools.text_tools import camelcase
from hspylib.modules.application.application import Application
from hspylib.modules.application.exit_status import ExitStatus

import atexit
import os
import sys

HERE = get_path(__file__)


class WidgetManager(metaclass=Singleton):
    """HsPyLib widget manager that handles HsPyLib widgets."""

    WIDGETS_PATH = HERE / "widgets"

    @staticmethod
    def _name_matches(expected_name: str, provided_name: str) -> bool:
        """Check if two names matches using defined naming rules.
        :param expected_name the expected widget name.
        :param provided_name the provided widget name (read from file).
        """

        return (
            expected_name.lower() == provided_name.lower()
            or expected_name == provided_name.capitalize()
            or expected_name == camelcase(provided_name, upper=True)
            or expected_name.lower() == provided_name.lower().replace("_", "")
        )

    def __init__(self, parent_app: Application):
        self._parent_app = parent_app
        self._widgets = []
        self._lookup_paths = os.environ.get("HHS_WIDGETS_PATH", "").split(":")
        self._lookup_paths.insert(0, str(WidgetManager.WIDGETS_PATH))
        list(map(sys.path.append, self._lookup_paths))
        check_state(self._search_widgets() > 0, "Unable to find any widgets from: {}", self._lookup_paths)

    def execute(self, widget_name: str, *widget_args) -> None:
        """Execute the specified widget.
        :param widget_name the widget name.
        :param widget_args the arguments to be provided to the widget.
        """

        widget = self._import_widget(camelcase(widget_name, upper=True))
        try:
            atexit.register(widget.cleanup)
            exit_code = widget.execute(*widget_args)
            if exit_code in [ExitStatus.ERROR, ExitStatus.FAILED]:
                raise WidgetExecutionError(f"Widget '{widget_name}' failed to execute. exit_code={exit_code}")
        except Exception as err:
            raise WidgetExecutionError(f"Unable to execute widget '{widget_name}' -> {err}") from err

    def dashboard(self) -> None:
        """Display all available widgets from the widget lookup paths on a dashboard."""

        items = []
        try:
            for widget_entry in self._widgets:
                widget = self._import_widget(widget_entry.name)
                item = DashboardItem(
                    widget.icon(), f"{widget.name()} v{widget.version()}: {widget.tooltip()}", widget.execute
                )
                items.append(item)
            check_state(len(items) > 0, "No widgets found from: {}", str(self._lookup_paths))
            mdashboard(items, "Please select a widget to execute")
        except Exception as err:
            raise WidgetExecutionError(f"Failed to execute widget :: {str(err)}") from err

    # pylint: disable=cell-var-from-loop
    def _search_widgets(self) -> int:
        """Search and load all widgets from the widget lookup paths."""

        for path in self._lookup_paths:
            for root, _, files in os.walk(path):
                filtered = list(filter(lambda p: p.startswith(WidgetEntry.MODULE_PREFIX) and p.endswith("py"), files))
                widgets = list(map(lambda w: WidgetEntry(w, f"{root}/{w}"), filtered))
                self._widgets.extend(widgets)

        return len(self._widgets)

    def _import_widget(self, widget_name: str) -> Widget:
        """Find, import and return a widget specified by the widget name.
        :param widget_name the widget name.
        """
        widget_entry = next((w for w in self._widgets if self._name_matches(widget_name, w.name)), None)
        if not widget_entry:
            raise WidgetNotFoundError(
                f"Widget '{widget_name}' was not found on widget lookup paths: {str(self._lookup_paths)}"
            )
        try:
            widget_module = __import__(widget_entry.module)
        except ModuleNotFoundError as err:
            raise WidgetNotFoundError(
                f"Widget '{widget_name}' was not found on widget lookup paths: {str(self._lookup_paths)}"
            ) from err
        widget_clazz = getattr(widget_module, widget_entry.clazz)
        widget = widget_clazz()
        check_state(isinstance(widget, Widget), 'All widgets must inherit from "clitt.addons.widman.Widget"')

        return widget
