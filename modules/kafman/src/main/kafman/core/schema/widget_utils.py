from abc import ABC
from typing import List, Type, Union

from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.qt.promotions.hcombobox import HComboBox
from hspylib.modules.qt.promotions.hlistwidget import HListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCheckBox, QDoubleSpinBox, QLineEdit, QSizePolicy, QSpinBox, QToolButton, QWidget

from kafman.core.schema.schema_field_type import SchemaFieldType


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
        'record': QToolButton,
        'object': QToolButton,
    }

    @staticmethod
    def get_widget(field_type: Union[str, SchemaFieldType]) -> Type[QWidget]:
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
        elif widget_type == QToolButton:
            WidgetUtils.setup_tool_button(widget)

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
    def setup_tool_button(widget: QToolButton) -> QWidget:
        WidgetUtils.setup_widget_commons(widget, "Click to fill")
        widget.setText(FormIcons.SELECTOR.value)
        widget.setMaximumWidth(30)
        widget.setMinimumHeight(30)

        return widget
