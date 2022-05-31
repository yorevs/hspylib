from typing import Optional, Union

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.field.schema_field_type import SchemaFieldType


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

    def get_value(self) -> Optional[dict]:
        pass
