from abc import ABC
from typing import List, Tuple, Type, Union

from hspylib.core.exception.exceptions import InvalidStateError
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.qt.promotions.hcombobox import HComboBox
from hspylib.modules.qt.promotions.hlistwidget import HListWidget
from hspylib.modules.qt.promotions.hstacked_widget import HStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCheckBox, QDoubleSpinBox, QFrame, QGridLayout, QLayout, QLineEdit, QPushButton, \
    QSizePolicy, \
    QSpinBox, \
    QToolButton, \
    QWidget

from kafman.core.schema.field.schema_field_type import SchemaFieldType


class WidgetUtils(ABC):

    QWIDGET_TYPE_MAP = {
        'boolean': QCheckBox,
        'integer': QSpinBox,
        'int': QSpinBox,
        'long': QSpinBox,
        'float': QDoubleSpinBox,
        'double': QDoubleSpinBox,
        'number': QDoubleSpinBox,
        'bytes': QLineEdit,
        'string': QLineEdit,
        'fixed': QLineEdit,
        'enum': HComboBox,
        'array': HListWidget,
        'record': None,
        'object': None,
    }

    @staticmethod
    def get_widget_type(field_type: Union[str, SchemaFieldType]) -> Type[QWidget]:
        return WidgetUtils.QWIDGET_TYPE_MAP[field_type.value] \
            if isinstance(field_type, SchemaFieldType) \
            else WidgetUtils.QWIDGET_TYPE_MAP[field_type]

    @staticmethod
    def setup_widget(
        widget: Union[QWidget, HComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QToolButton, QCheckBox, HListWidget],
        doc: str = None,
        symbols: list = None,
        default: Union[str, int, float, bool] = None) -> QWidget:
        """Return the QWidget that the field is displayed at the schema form"""

        widget_type = widget.__class__
        tooltip = doc
        if widget_type == HComboBox:
            WidgetUtils.setup_combo_box(widget, symbols, tooltip, default)
        elif widget_type == HListWidget:
            WidgetUtils.setup_list(widget, tooltip, default)
        elif widget_type == QCheckBox:
            WidgetUtils.setup_checkbox(widget, tooltip, default)
        elif widget_type in [QSpinBox, QDoubleSpinBox]:
            WidgetUtils.setup_spin_box(widget, tooltip, default)
        elif widget_type == QLineEdit:
            WidgetUtils.setup_line_edit(widget, tooltip)
        else:
            raise InvalidStateError(f'Widget type "{widget_type.name}" is not supported')

        return widget

    @staticmethod
    def setup_widget_commons(widget: QWidget, tooltip: str) -> QWidget:
        widget.setToolTip(tooltip)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        widget.setStyleSheet('QWidget {padding: 5px;}')
        widget.setFont(QFont("DroidSansMono Nerd Font", 14))
        widget.setMinimumHeight(35)

        return widget

    @staticmethod
    def setup_combo_box(
        widget: HComboBox,
        symbols: List[str],
        tooltip: str = None,
        default: str = None) -> QWidget:

        widget.addItems(symbols or default or [])
        widget.setEditable(True)
        widget.lineEdit().setPlaceholderText(tooltip)
        widget.setCurrentText(default or widget.itemText(0))

        return WidgetUtils.setup_widget_commons(widget, tooltip)

    @staticmethod
    def setup_list(
        widget: HListWidget,
        tooltip: str = None,
        default: str = None) -> QWidget:

        widget.addItems(default or [])
        widget.set_editable()

        return WidgetUtils.setup_widget_commons(widget, tooltip)

    @staticmethod
    def setup_checkbox(
        widget: QCheckBox,
        tooltip: str = None,
        default: Union[int, float] = False) -> QWidget:

        widget.setChecked(default or False)

        return WidgetUtils.setup_widget_commons(widget, tooltip)

    @staticmethod
    def setup_spin_box(
        widget: QSpinBox,
        tooltip: str = None,
        default: Union[int, float] = 0) -> QWidget:

        min_val, max_val = 0, 9999
        widget.setMinimum(min_val)
        widget.setMaximum(max_val)
        widget.setValue(default or 0)
        widget.setLayoutDirection(Qt.RightToLeft)

        return WidgetUtils.setup_widget_commons(widget, tooltip)

    @staticmethod
    def setup_line_edit(
        widget: QLineEdit,
        tooltip: str = None,
        default: str = '') -> QWidget:

        widget.setPlaceholderText(tooltip)
        widget.setText(default or '')

        return WidgetUtils.setup_widget_commons(widget, tooltip)

    @staticmethod
    def create_goto_form_button(index : int, form_stack: HStackedWidget) -> QPushButton:
        tool_button = QPushButton(FormIcons.ARROW_RIGHT.value + " Fill")
        tool_button.clicked.connect(lambda: form_stack.slide_to_index(index))
        WidgetUtils.setup_widget_commons(tool_button, f'Click to fill the form')
        tool_button.setMaximumWidth(100)
        tool_button.setMinimumHeight(30)
        tool_button.setDefault(False)
        tool_button.setAutoDefault(False)

        return tool_button

    @staticmethod
    def create_back_button(index : int, form_stack: HStackedWidget) -> QPushButton:
        tool_button = QPushButton(FormIcons.ARROW_LEFT.value + " Back")
        tool_button.clicked.connect(lambda: form_stack.slide_to_index(index))
        WidgetUtils.setup_widget_commons(tool_button, "Click to go to previous form")
        tool_button.setMaximumWidth(100)
        tool_button.setMinimumHeight(30)
        tool_button.setDefault(False)
        tool_button.setAutoDefault(False)

        return tool_button

    @classmethod
    def create_form_pane(cls, form_stack: HStackedWidget, form_name: str) -> Tuple[QFrame, QGridLayout]:
        form_pane = QFrame(form_stack)
        form_pane.setContentsMargins(0, 0, 0, 0)
        form_pane.setObjectName(form_name)
        layout = QGridLayout(form_pane)
        form_pane.setLayout(layout)

        return form_pane, layout
