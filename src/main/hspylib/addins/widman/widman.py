import os
import sys
from typing import Any

from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import get_path

HERE = get_path(__file__)


class WidgetManager(metaclass=Singleton):
    """TODO"""

    WIDGETS_PATH = (HERE / "widgets")

    WIDGET_PREFIX = 'widget_'

    class WidgetEntry:
        def __init__(self, file: str, path: str):
            self.name = os.path.splitext(file)[0].replace(WidgetManager.WIDGET_PREFIX, '').capitalize()
            self.clazz = f"Widget{self.name}"
            self.path = path

        def __str__(self):
            return f"{self.name}:{self.clazz} => {self.path}"

    def __init__(self, parent: Any):
        self._parent = parent
        self._widgets = []
        self._lookup_paths = os.environ.get('HHS_WIDGETS_PATH', '').split(':')
        self._lookup_paths.insert(0, str(WidgetManager.WIDGETS_PATH))
        list(map(sys.path.append, self._lookup_paths))
        self._load_widgets()

    def execute(self, widget_name: str) -> Any:
        print(f'Executing widget: {widget_name}')
        print('Paths: {}'.format(*self._lookup_paths))

    def list(self) -> None:
        """List all widgets from the lookup paths"""
        print('Listing all widgets')
        print('')
        print('\n'.join(list(map(lambda w: f"Name: {w.name}, Class: {w.clazz}, Path: {w.path}", self._widgets))))
        print('')

    def _load_widgets(self):
        """Search and load all widgets from the lookup paths"""
        for path in self._lookup_paths:
            for root, _, files in os.walk(path):
                filtered = [ f for f in list(filter(lambda p: p.startswith(self.WIDGET_PREFIX), files)) ]
                widgets = list(
                    map(lambda w: self.WidgetEntry(w, f"{root}/{w}"), filtered)
                )
                self._widgets.extend(widgets)
