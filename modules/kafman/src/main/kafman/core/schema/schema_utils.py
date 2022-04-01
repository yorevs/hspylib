from abc import ABC
from typing import Any, List

from hspylib.core.exception.exceptions import InvalidStateError

from kafman.core.schema.schema_field import SchemaField
from kafman.core.schema.schema_field_type import SchemaFieldType


class SchemaUtils(ABC):

    @staticmethod
    def check_and_get(attribute: str, content: dict = None, required: bool = True, default: Any = None) -> Any:
        if content and attribute in content:
            return content[attribute]
        else:
            if required:
                raise InvalidStateError(f'Required attribute {attribute} was not found in content string !')

        return default

    @staticmethod
    def parse_field(field: dict) -> 'SchemaField':
        """TODO"""
        field_name = SchemaUtils.check_and_get('name', field, True)
        field_type = SchemaUtils.check_and_get('type', field, True)
        field_doc = SchemaUtils.check_and_get('doc', field, False, f'the {field_name}')
        field_default = SchemaUtils.check_and_get('default', field, False, None)
        required = 'null' not in field_type
        avro_type = SchemaFieldType.of_type(field_type)
        if avro_type.is_complex():
            return SchemaField.of_complex(field_name, field_doc, field_type, field_default, required)
        elif avro_type.is_primitive():
            return SchemaField.of_primitive(field_name, field_doc, avro_type, field_default, required)
        elif avro_type.is_enum():
            symbols = SchemaUtils.check_and_get('symbols', field, True)
            return SchemaField.of_enum(field_name, field_doc, symbols, field_default, required)
        elif avro_type.is_array():
            items = SchemaUtils.check_and_get('items', field, True)
            return SchemaField.of_array(field_name, field_doc, items, field_default, required)
        elif avro_type.is_map():
            values = SchemaUtils.check_and_get('values', field, True)
            return SchemaField.of_array(field_name, field_doc, values, field_default, required)
        else:
            raise InvalidStateError(f'Invalid field type: {avro_type}')

    @staticmethod
    def parse_record(fields: List[dict]) -> List[SchemaField]:
        """TODO"""
        record_fields = []
        for next_field in fields:
            field = SchemaUtils.parse_field(next_field)
            record_fields.append(field)

        return record_fields
