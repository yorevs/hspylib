from typing import List

from PyQt5.QtWidgets import QWidget

from kafman.core.schema.json.json_type import JsonType
from kafman.core.schema.schema_field import SchemaField
from kafman.core.schema.widget_utils import WidgetUtils


class ArrayProperty(SchemaField):

    def __init__(
        self,
        name: str,
        description: str,
        a_items: List[str],
        required: bool = True):
        super().__init__(
            name,
            description,
            JsonType.ARRAY,
            required=required)

        self.a_items = a_items

    def create_input_widget(self) -> QWidget:
        self.widget = WidgetUtils.get_widget_type(self.a_type.value)()
        return WidgetUtils.setup_list(self.widget, self.a_items, self.doc)