from typing import List, Union, Optional

from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit

from hspylib.modules.qt.promotions.hcombobox import HComboBox


class SchemaField:
    """TODO"""

    QWIDGET_TYPE_MAP = {
        'int': QSpinBox,
        'long': QSpinBox,
        'float': QDoubleSpinBox,
        'double': QDoubleSpinBox,
        'boolean': QCheckBox,
        'string': QLineEdit,
        'bytes': QLineEdit,
        'array': HComboBox
    }

    @staticmethod
    def of_dict(field: dict, required: bool) -> 'SchemaField':
        """TODO"""
        return SchemaField(
            field['name'],
            field['type'],
            required,
        )

    @staticmethod
    def of_map(field_name: str, field_attrs: dict, required: bool) -> 'SchemaField':
        """TODO"""
        return SchemaField(
            field_name,
            field_attrs['type'],
            required
        )

    def value_from(self, widget: Union[QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit]) -> dict:
        """TODO"""
        if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            value = str(widget.value())
        elif isinstance(widget, QCheckBox):
            value = str(bool(widget.get()))
        else:
            value = widget.text()

        return { self._name: value }

    def __init__(self, name: str, ftype: Union[str, list], required: bool):
        self._name = name
        self._type = next((typ for typ in ftype if typ != 'null'), None)\
            if isinstance(ftype, list) \
            else ftype
        self._required = required
        self._widget_type = self.QWIDGET_TYPE_MAP[self._type] \
            if self._type in self.QWIDGET_TYPE_MAP \
            else QLineEdit

    def __str__(self):
        return f"name={self._name}, type={self._type}, required={self._required}, widget={self._widget_type.__class__}"

    def get_name(self) -> str:
        """TODO"""
        return self._name

    def get_type(self) -> Union[str, list]:
        """TODO"""
        return self._type

    def is_required(self) -> bool:
        """TODO"""
        return self._required

    def get_symbols(self) -> Optional[List[str]]:
        """TODO"""
        return self._symbols

    def widget(self) -> Union[QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit]:
        """TODO"""
        widget_instance = self._widget_type()
        if self._widget_type == QLineEdit:
            widget_instance.setPlaceholderText(f"This field is {'required' if self._required else 'optional'}")
        elif self._widget_type == HComboBox:
            widget_instance.lineEdit().setPlaceholderText(f"Please type in the items")
            widget_instance.setEditable(True)
        return widget_instance
