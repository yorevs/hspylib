import json
from collections import defaultdict

from hspylib.core.tools.text_tools import strip_extra_spaces, strip_linebreaks
from hspylib.modules.qt.promotions.hstacked_widget import HStackedWidget
from PyQt5.QtWidgets import QScrollArea, QWidget


class FormArea(QScrollArea):
    """TODO"""

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._form = None

    def setWidget(self, widget: QWidget) -> None:
        if self._form is not None:
            assert isinstance(widget, HStackedWidget), 'Only HStackedWidget type instances are accepted'
        super().setWidget(widget)
        self._form = widget

    def get_form(self) -> HStackedWidget:
        """TODO"""
        return self._form

    def values(self) -> str:
        """TODO"""

        root = defaultdict()
        current = None
        for pane in self._form.widgets():
            if current is None:
                current = root
                root.update(pane.fields())
            else:
                current = pane[pane.parent_name()].fields()[pane.name()]
                current.update(pane.fields())


        return strip_extra_spaces(strip_linebreaks(json.dumps(root, indent=0)))
