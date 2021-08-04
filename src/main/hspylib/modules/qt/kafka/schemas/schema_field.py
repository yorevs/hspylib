from typing import Union, List, Type, Optional

from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit, QWidget

from hspylib.core.tools.commons import get_by_key_or_default
from hspylib.modules.qt.promotions.hcombobox import HComboBox


class SchemaField:
    """TODO"""

    # Avro Types: https://avro.apache.org/docs/current/spec.html#schema_record
    # Json Types: https://json-schema.org/understanding-json-schema/reference/type.html
    QWIDGET_TYPE_MAP = {
        'int': QSpinBox,
        'integer': QSpinBox,
        'long': QSpinBox,
        'float': QDoubleSpinBox,
        'double': QDoubleSpinBox,
        'number': QDoubleSpinBox,
        'boolean': QCheckBox,
        'string': QLineEdit,
        'bytes': QLineEdit,
        'array': HComboBox,
        'enum': HComboBox,
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

    def __init__(
        self,
        name: str,
        field_type: Union[str, list],
        required: bool,
        field_attrs: dict):

        self._name = name
        self._type = next((typ for typ in field_type if typ != 'null'), None)\
            if isinstance(field_type, list) \
            else field_type
        self._required = required
        self._field_attrs = field_attrs
        self._widget_type = self._widget_type()

    def __str__(self):
        return f"name={self._name}, type={self._type}, required={self._required}, widget={self._widget_type.__class__}"

    def get_field_value(self, widget_instance: QWidget) -> Optional[dict]:
        """TODO"""
        if isinstance(widget_instance, (QSpinBox, QDoubleSpinBox)):
            value = str(widget_instance.value())
        elif isinstance(widget_instance, QCheckBox):
            value = str(bool(widget_instance.get()))
        elif isinstance(widget_instance, HComboBox):
            value = str(bool(widget_instance.currentText()))
        else:
            value = widget_instance.text()

        return { self._name: value } if value else None

    def is_valid(self, widget_instance: QWidget) -> bool:
        """TODO"""
        return not self.is_required() or self.get_field_value(widget_instance) is not None

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
        default_value = get_by_key_or_default(self._field_attrs, 'default', '')
        tooltip = get_by_key_or_default(self._field_attrs, 'examples')
        tooltip = ('Examples: \n' + '\n'.join([f'  - {str(t)}' for t in tooltip])) \
            if tooltip \
            else self._placeholder_text()
        widget_instance.setToolTip(tooltip)
        if self._widget_type == QLineEdit:
            widget_instance.setPlaceholderText(self._placeholder_text())
            widget_instance.setText(default_value)
        elif self._widget_type == HComboBox:
            widget_instance.addItems(self._field_items())
            widget_instance.setEditable(True)
            widget_instance.lineEdit().setPlaceholderText(self._placeholder_text())
            widget_instance.setCurrentText(default_value)
        elif self._widget_type == HComboBox:
            widget_instance.setValue(default_value)
        elif self._widget_type == QCheckBox:
            widget_instance.setChecked(bool(default_value))

        return widget_instance

    def _widget_type(self) -> Type[QWidget]:
        """TODO"""
        return self.QWIDGET_TYPE_MAP[self._type] \
            if self._type in self.QWIDGET_TYPE_MAP \
            else QLineEdit

    def _field_items(self) -> List[str]:
        """TODO"""
        enums = None
        if self._field_attrs['type'] == 'array':
            items = get_by_key_or_default(self._field_attrs, 'items')
            enums = get_by_key_or_default(items, 'enum')
        elif self._field_attrs['type'] == 'enum':
            enums = get_by_key_or_default(self._field_attrs, 'symbols')
        return enums or []

    def _placeholder_text(self) -> str:
        """TODO"""
        text = get_by_key_or_default(self._field_attrs, 'description')
        text = get_by_key_or_default(self._field_attrs, 'doc') if not text else text
        text = f"This field is {'required' if self._required else 'optional'}" if not text else text
        return text
