from typing import List

from hspylib.modules.qt.promotions.hcombobox import HComboBox
from PyQt5.QtWidgets import QWidget

from kafman.core.schema.json.json_type import JsonType
from kafman.core.schema.schema_field import SchemaField
from kafman.core.schema.widget_utils import WidgetUtils


class ArrayProperty(SchemaField):

    def __init__(
        self,
        name: str,
        description: str,
        all_items: List[str],
        default: str = None,
        required: bool = True):
        super().__init__(
            name,
            description,
            JsonType.ARRAY,
            default,
            required)

        self.all_items = all_items

    def create_input_widget(self) -> QWidget:
        self.widget: HComboBox = WidgetUtils.get_widget_type('enum')()
        return WidgetUtils.setup_combo_box(self.widget, self.all_items, self.doc)
