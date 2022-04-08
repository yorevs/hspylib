from typing import Any, Optional, Union

from hspylib.core.exception.exceptions import InvalidStateError
from hspylib.modules.qt.promotions.hcombobox import HComboBox
from PyQt5.QtWidgets import QToolButton, QWidget

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.schema_field_type import SchemaFieldType
from kafman.core.schema.widget_utils import WidgetUtils


class ComplexField(SchemaField):

    def __init__(
        self,
        name: str,
        doc: str,
        complex_types: Union[list, dict],
        default: Any = None,
        required: bool = True):

        super().__init__(
            name,
            doc,
            SchemaFieldType.COMPLEX,
            default,
            required=required)

        self.complex_types = complex_types

    def create_input_widget(self) -> QWidget:
        if isinstance(self.complex_types, list):
            types = list(filter(lambda f: f != 'null', self.complex_types))
            if len(types) > 1:
                raise InvalidStateError('Multi-type is not supported yet')
            else:
                return self._setup_complex_widget(types[0])
        elif isinstance(self.complex_types, dict):
            return self._setup_complex_widget(self.complex_types)

    def get_value(self) -> Optional[dict]:
        pass

    def _setup_complex_widget(self, complex_object: dict) -> QWidget:
        """TODO"""

        c_type = complex_object['type']
        widget_type = WidgetUtils.get_widget(c_type) \
            if c_type not in ['record', 'complex'] else None
        if widget_type is None:
            self.widget = QToolButton()
            return WidgetUtils.setup_tool_button(self.widget)
        elif widget_type == HComboBox:
            c_symbols = complex_object['symbols']
            self.widget = widget_type()
            WidgetUtils.setup_combo_box(self.widget, c_symbols, self.doc, self.default)
        else:
            raise InvalidStateError(f'WidgetType {widget_type} is not supported yet')

        return self.widget
