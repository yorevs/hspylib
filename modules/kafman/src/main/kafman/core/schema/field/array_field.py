from typing import List, Optional

from PyQt5.QtWidgets import QWidget

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.schema_field_type import SchemaFieldType


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
        pass

    def get_value(self) -> Optional[dict]:
        pass
