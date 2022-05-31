from typing import Optional

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.field.schema_field_type import SchemaFieldType


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

    def get_value(self) -> Optional[dict]:
        pass
