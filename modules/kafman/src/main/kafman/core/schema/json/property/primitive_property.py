from typing import Any

from kafman.core.schema.json.json_type import JsonType
from kafman.core.schema.schema_field import SchemaField


class PrimitiveProperty(SchemaField):

    def __init__(
        self,
        name: str,
        description: str,
        p_type: JsonType,
        default: Any = None,
        required: bool = True):
        super().__init__(
            name,
            description,
            p_type,
            default,
            required)
