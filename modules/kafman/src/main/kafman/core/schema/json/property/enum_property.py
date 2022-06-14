from typing import List

from PyQt5.QtWidgets import QWidget

from kafman.core.schema.json.json_type import JsonType
from kafman.core.schema.schema_field import SchemaField
from kafman.core.schema.widget_utils import WidgetUtils


class EnumProperty(SchemaField):

    def __init__(
        self,
        name: str,
        description: str,
        symbols: List[str],
        default: str,
        required: bool = True):
        super().__init__(
            name,
            description,
            JsonType.ENUM,
            default,
            required)

        self.symbols = symbols

    def create_input_widget(self) -> QWidget:
        self.widget = WidgetUtils.get_widget_type(self.a_type.value)()
        return WidgetUtils.setup_combo_box(self.widget, self.symbols, self.doc)
