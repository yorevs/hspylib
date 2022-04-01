from abc import ABC
from typing import Any, List, Union

from hspylib.core.exception.exceptions import InvalidStateError
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.qt.promotions.hcombobox import HComboBox
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
        'array': HComboBox,
        'record': QToolButton,
        'object': QToolButton,
        'complex': QToolButton,
    }

    @staticmethod
    def create_input_widget(
        field_type: SchemaFieldType,
        complex_type: dict,
        doc: str,
        default: Any) -> QWidget:
        """Return the QWidget type required by this field"""

        if field_type.value not in WidgetUtils.QWIDGET_TYPE_MAP:
            raise InvalidStateError(f'Unrecognized field type: {field_type}')

        return WidgetUtils.QWIDGET_TYPE_MAP[field_type.value]() \
            if not complex_type \
            else WidgetUtils.create_complex_type_widget(complex_type, doc, default)

    @staticmethod
    def create_complex_type_widget(
        complex_types: Union[list, dict],
        doc: str,
        default: Any) -> QWidget:
        """TODO"""

        if isinstance(complex_types, list):
            types = list(filter(lambda f: f != 'null', complex_types))
            if len(types) > 1:
                raise InvalidStateError('Multi-type is not supported yet')
            else:
                return WidgetUtils.setup_complex_widget(types[0], doc, default)
        elif isinstance(complex_types, dict):
            return WidgetUtils.setup_complex_widget(complex_types, doc, default)

    @staticmethod
    def setup_complex_widget(complex_object: dict, doc: str, default: Any) -> QWidget:
        """TODO"""

        c_type = complex_object['type']
        widget_type = WidgetUtils.QWIDGET_TYPE_MAP[c_type] \
            if c_type not in ['record', 'complex'] else QToolButton
        if widget_type == HComboBox:
            c_symbols = complex_object['symbols']
            widget = widget_type()
            WidgetUtils.setup_combo_box(widget, c_symbols, doc, default)
            return widget
        elif widget_type == QToolButton:
            btn_fill_record = widget_type()
            return WidgetUtils.setup_tool_button(btn_fill_record)
        else:
            raise InvalidStateError(f'WidgetType {widget_type} is not supported yet')

    @staticmethod
    def setup_widget(
        widget: QWidget,
        doc: str = None,
        symbols: list = None,
        default: Union[str, int, float, bool] = None) -> QWidget:
        """Return the QWidget that the field is displayed at the schema form"""

        widget_type = widget.__class__
        tooltip = doc
        if widget_type == HComboBox:
            WidgetUtils.setup_combo_box(widget, symbols, tooltip, default)
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
        widget: QWidget,
        symbols: List[str],
        tooltip: str = None,
        default: str = None) -> QWidget:

        widget.addItems(symbols or [])
        widget.setEditable(True)
        widget.lineEdit().setPlaceholderText(tooltip)
        widget.setCurrentText(default or widget.itemText(0))
        WidgetUtils.setup_widget_commons(widget, tooltip)

        return widget

    @staticmethod
    def setup_checkbox(
        widget: QWidget,
        tooltip: str = None,
        default: Union[int, float] = None) -> QWidget:

        widget.setChecked(default)
        WidgetUtils.setup_widget_commons(widget, tooltip)

        return widget

    @staticmethod
    def setup_spin_box(
        widget: QWidget,
        tooltip: str = None,
        default: Union[int, float] = None) -> QWidget:

        min_val, max_val = 0.0, 9999.999
        widget.setMinimum(min_val)
        widget.setMaximum(max_val)
        widget.setValue(default or 0)
        widget.setLayoutDirection(Qt.RightToLeft)
        WidgetUtils.setup_widget_commons(widget, tooltip)

        return widget

    @staticmethod
    def setup_line_edit(
        widget: QWidget,
        tooltip: str = None,
        default: str = None) -> QWidget:

        widget.setPlaceholderText(tooltip)
        widget.setText(default or '')
        WidgetUtils.setup_widget_commons(widget, tooltip)

        return widget

    @staticmethod
    def setup_tool_button(widget: QWidget) -> QWidget:
        WidgetUtils.setup_widget_commons(widget, "Click to fill")
        widget.setText(FormIcons.SELECTOR.value)
        widget.setMaximumWidth(30)
        widget.setMinimumHeight(30)

        return widget
