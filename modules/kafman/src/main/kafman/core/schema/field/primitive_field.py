from typing import Any, Optional

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.field.schema_field_type import SchemaFieldType


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

    def get_value(self) -> Optional[dict]:
        pass
