from typing import Tuple

from kafman.core.schema.json.json_type import JsonType
from kafman.core.schema.json.property.property import Property
from kafman.core.schema.schema_field import SchemaField


class ObjectProperty(SchemaField):

    def __init__(
        self,
        name: str,
        description: str,
        properties: Tuple[Property],
        required: bool = True):
        super().__init__(
            name,
            description,
            JsonType.OBJECT,
            required=required)

        self.properties = properties
