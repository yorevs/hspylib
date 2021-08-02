from typing import Union, List, Type

from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit, QWidget

from hspylib.core.tools.commons import get_by_key_or_default
from hspylib.modules.qt.promotions.hcombobox import HComboBox


class SchemaField:
    """TODO"""

    QWIDGET_TYPE_MAP = {
        'int': QSpinBox,
        'integer': QSpinBox,
        'long': QSpinBox,
        'float': QDoubleSpinBox,
        'double': QDoubleSpinBox,
        'boolean': QCheckBox,
        'string': QLineEdit,
        'bytes': QLineEdit,
        'array': HComboBox
    }

    @staticmethod
    def of_dict(field_attrs: dict, required: bool = True) -> 'SchemaField':
        """TODO"""
        return SchemaField(
            field_attrs['name'],
            field_attrs['type'],
            required,
            field_attrs
        )

    @staticmethod
    def of_map(field_name: str, field_attrs: dict, required: bool = True) -> 'SchemaField':
        """TODO"""
        return SchemaField(
            field_name,
            field_attrs['type'],
            required,
            field_attrs
        )

    def __init__(self, name: str, field_type: Union[str, list], required: bool, field_attrs: dict):
        self._name = name
        self._type = next((typ for typ in field_type if typ != 'null'), None)\
            if isinstance(field_type, list) \
            else field_type
        self._required = required
        self._field_attrs = field_attrs
        self._widget_type = self._widget_type()

    def __str__(self):
        return f"name={self._name}, type={self._type}, required={self._required}, widget={self._widget_type.__class__}"

    def value_from(self, widget: Union[QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit, HComboBox]) -> dict:
        """TODO"""
        if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            value = str(widget.value())
        elif isinstance(widget, QCheckBox):
            value = str(bool(widget.get()))
        elif isinstance(widget, HComboBox):
            value = str(bool(widget.currentText()))
        else:
            value = widget.text()

        return { self._name: value }

    def get_name(self) -> str:
        """TODO"""
        return self._name

    def get_type(self) -> Union[str, list]:
        """TODO"""
        return self._type

    def is_required(self) -> bool:
        """TODO"""
        return self._required

    def widget(self) -> QWidget:
        """TODO"""
        widget_instance = self._widget_type()
        if self._widget_type == QLineEdit:
            widget_instance.setPlaceholderText(self._placeholder_text())
        elif self._widget_type == HComboBox:
            widget_instance.addItems(self._field_items())
            widget_instance.setEditable(True)
            widget_instance.lineEdit().setPlaceholderText(self._placeholder_text())
        return widget_instance

    def _widget_type(self) -> Type[QWidget]:
        """TODO"""
        return self.QWIDGET_TYPE_MAP[self._type] \
            if self._type in self.QWIDGET_TYPE_MAP \
            else QLineEdit

    def _field_items(self) -> List[str]:
        """TODO"""
        items = get_by_key_or_default(self._field_attrs, 'items')
        enums = get_by_key_or_default(items, 'enum')
        return enums or []

    def _placeholder_text(self) -> str:
        """TODO"""
        text = get_by_key_or_default(self._field_attrs, 'description')
        text = get_by_key_or_default(self._field_attrs, 'doc') if not text else text
        text = f"This field is {'required' if self._required else 'optional'}" if not text else text
        return text
