from typing import Any, Optional

from PyQt5.QtWidgets import QWidget

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.schema_field_type import SchemaFieldType
from kafman.core.schema.widget_utils import WidgetUtils


class PrimitiveField(SchemaField):

    def __init__(
        self,
        name: str,
        doc: str,
        p_type: SchemaFieldType,
        default: Any = None,
        required: bool = True):

        super().__init__(
            name,
            doc,
            p_type,
            default,
            required=required)

    def create_input_widget(self) -> QWidget:
        self.widget = WidgetUtils.get_widget(self.a_type)()
        return WidgetUtils.setup_widget(self.widget, self.doc, default=self.default)

    def get_value(self) -> Optional[dict]:
        pass
