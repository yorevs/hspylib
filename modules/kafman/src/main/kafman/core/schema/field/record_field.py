from typing import Optional, Union

from PyQt5.QtWidgets import QToolButton, QWidget

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.schema_field_type import SchemaFieldType
from kafman.core.schema.widget_utils import WidgetUtils


class RecordField(SchemaField):

    def __init__(
        self,
        name: str,
        doc: str,
        fields: Union[list, dict],
        required: bool = True):

        super().__init__(
            name,
            doc,
            SchemaFieldType.RECORD,
            required=required)

        self.fields = fields

    def create_input_widget(self) -> QWidget:
        self.widget = QToolButton()
        return WidgetUtils.setup_tool_button(self.widget)

    def get_value(self) -> Optional[dict]:
        pass
