import os
import sys
from typing import Any, List

from hspylib.addons.widman.widget import Widget
from hspylib.core.enums.exit_code import ExitCode
from hspylib.core.exception.exceptions import WidgetNotFoundError, WidgetExecutionError
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import get_path, syserr
from hspylib.core.tools.text_helper import camelcase
from hspylib.modules.cli.menu.extra.mdashboard import MenuDashBoard, mdashboard

HERE = get_path(__file__)


class WidgetManager(metaclass=Singleton):
    """TODO"""

    WIDGETS_PATH = (HERE / "widgets")

    WIDGET_PREFIX = 'widget_'

    class WidgetEntry:
        def __init__(self, file: str, path: str):
            self.module = os.path.splitext(file)[0]
            self.name = camelcase(self.module.replace(WidgetManager.WIDGET_PREFIX, ''))
            self.clazz = f"Widget{self.name.replace('_', '')}"
            self.path = path

        def __str__(self):
            return f"{self.name}: {self.module}.{self.clazz} => {self.path}"

    def __init__(self, parent: Any):
        self._parent = parent
        self._widgets = []
        self._lookup_paths = os.environ.get('HHS_WIDGETS_PATH', '').split(':')
        self._lookup_paths.insert(0, str(WidgetManager.WIDGETS_PATH))
        list(map(sys.path.append, self._lookup_paths))
        self._load_widgets()

    def execute(self, widget_name: str, widget_args: List[Any]) -> Any:
        """Execute the specified widget"""
        widget = self._find_widget(camelcase(widget_name))
        try:
            exit_code = widget.execute(*widget_args)
            if exit_code == ExitCode.SUCCESS:
                widget.cleanup()
            else:
                raise WidgetExecutionError(f"Widget '{widget_name}' failed to execute. exit_code={exit_code}")
        except Exception as err:
            syserr("Current widget paths: \n{}".format('\n'.join(self._lookup_paths)))
            raise WidgetExecutionError(f"Unable to execute widget '{widget_name}' -> {err}") from err

    def dashboard(self) -> None:
        """Display all available widgets from the lookup paths"""
        items = []
        widget_entry = None
        try:
            for widget_entry in self._widgets:
                widget = self._find_widget(widget_entry.name)
                item = MenuDashBoard.DashBoardItem(
                    widget.icon(),
                    f"{widget.name()} v{widget.version()}: {widget.tooltip()}",
                    widget.execute
                )
                items.append(item)
            mdashboard(items, 6, 'Please select a widget to execute')
        except Exception as err:
            syserr("Current widget paths: \n{}".format('\n'.join(self._lookup_paths)))
            raise WidgetExecutionError(f"Unable to access widget '{widget_entry.name}' -> {err}") from err

    def _load_widgets(self):
        """Search and load all widgets from the lookup paths"""
        for path in self._lookup_paths:
            for root, _, files in os.walk(path):
                filtered = list(filter(
                    lambda p: p.startswith(self.WIDGET_PREFIX) and p.endswith('py'), files)
                )
                widgets = list(
                    map(lambda w: self.WidgetEntry(w, f"{root}/{w}"), filtered)
                )
                self._widgets.extend(widgets)

    def _find_widget(self, widget_name: str):
        widget_entry = next((w for w in self._widgets if self.name_matches(widget_name, w.name)), None)
        if not widget_entry:
            raise WidgetNotFoundError(
                f"Widget '{widget_name}' was not found on configured paths: {str(self._lookup_paths)}")
        try:
            widget_module = __import__(widget_entry.module)
        except ModuleNotFoundError as err:
            raise WidgetNotFoundError(
                f"Widget '{widget_name}' was not found on configured paths: {str(self._lookup_paths)}") from err
        widget_clazz = getattr(widget_module, widget_entry.clazz)
        widget = widget_clazz()
        assert isinstance(widget, Widget), \
            'All widgets must inherit from "hspylib.addons.widman.widget.Widget"'
        return widget

    @staticmethod
    def name_matches(widget_1_name: str, widget_2_name: str):
        return \
            widget_1_name.lower() == widget_2_name.lower() \
            or widget_1_name == widget_2_name.capitalize() \
            or widget_1_name == camelcase(widget_2_name) \
            or widget_1_name.lower() == widget_2_name.lower().replace('_', '')

