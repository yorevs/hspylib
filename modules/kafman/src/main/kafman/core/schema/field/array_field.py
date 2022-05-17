from typing import List, Optional

from PyQt5.QtWidgets import QWidget

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.schema_field_type import SchemaFieldType
from kafman.core.schema.widget_utils import WidgetUtils


class ArrayField(SchemaField):

    def __init__(
        self,
        name: str,
        doc: str,
        items: List[str],
        default: str = None,
        required: bool = True):

        super().__init__(
            name,
            doc,
            SchemaFieldType.ARRAY,
            default,
            required=required)

        self.items = items

    def create_input_widget(self) -> QWidget:
        self.widget = WidgetUtils.get_widget(self.a_type)()
        return WidgetUtils.setup_widget(self.widget, self.doc, self.items, default=self.default)

    def get_value(self) -> Optional[dict]:
        pass
