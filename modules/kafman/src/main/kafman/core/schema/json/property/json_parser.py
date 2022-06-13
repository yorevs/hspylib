from abc import ABC
from typing import List, Tuple

from hspylib.core.tools.preconditions import check_and_get

from kafman.core.schema.json.json_type import JsonType
from kafman.core.schema.json.property.property import Property


class JsonParser(ABC):
    """TODO"""

    class JsonSchemaData:
        """TODO"""

        def __init__(self):
            self.id = None
            self.schema = None
            self.title = None
            self.description = None
            self.properties = None
            self.required = None
            self.type = None

    @staticmethod
    def parse(json_dict: dict) -> 'JsonSchemaData':
        """TODO"""

        schema = JsonParser.JsonSchemaData()
        schema.id = check_and_get('$id', json_dict)
        schema.schema = check_and_get('$schema', json_dict)
        schema.title = check_and_get('title', json_dict)
        schema.description = check_and_get('description', json_dict, False)
        schema.required = check_and_get('required', json_dict, False, [])
        schema.type = check_and_get('type', json_dict)

        if 'object' == schema.type:
            properties = check_and_get('properties', json_dict, default={})
            schema.properties = JsonParser._parse_properties(properties, schema.required)

        return schema

    @staticmethod
    def _parse_properties(properties: dict, required: List[str]) -> Tuple[Property]:
        """TODO"""

        schema_properties = []
        for p_name, props in properties.items():
            p_title = check_and_get('title', props, False, '')
            p_description = check_and_get('description', props, False, '')
            p_type = JsonType.of_value(check_and_get('type', props))
            p_default = check_and_get('default', props, False)
            p_required = p_name in required

            p_properties = JsonParser._parse_properties(check_and_get('properties', props), required) \
                if p_type == JsonType.OBJECT else None
            p_symbols = check_and_get('enum', props['items'], False, []) \
                if p_type == JsonType.ARRAY else None

            prop = Property(p_name, p_title, p_description, p_type, p_default, p_required)
            prop.all_properties = p_properties
            prop.all_symbols = p_symbols
            schema_properties.append(prop)

        return tuple(schema_properties)
