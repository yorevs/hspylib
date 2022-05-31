from typing import Optional

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.field.schema_field_type import SchemaFieldType


class FixedField(SchemaField):

    def __init__(
        self,
        name: str,
        doc: str,
        size: int):

        super().__init__(
            name,
            doc,
            SchemaFieldType.FIXED,
            default=size)

    def get_value(self) -> Optional[dict]:
        pass
