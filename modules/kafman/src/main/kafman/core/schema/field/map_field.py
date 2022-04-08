from typing import Optional

from PyQt5.QtWidgets import QWidget

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.schema_field_type import SchemaFieldType


class MapField(SchemaField):

    def __init__(
        self,
        name: str,
        doc: str,
        values: dict,
        default: str = None,
        required: bool = True):

        super().__init__(
            name,
            doc,
            SchemaFieldType.MAP,
            default, required=required)

        self.values = values

    def create_input_widget(self) -> QWidget:
        pass

    def get_value(self) -> Optional[dict]:
        pass
