from abc import ABC
from typing import List

from hspylib.core.exception.exceptions import InvalidStateError

from kafman.core.schema.field.array_field import ArrayField
from kafman.core.schema.field.complex_field import ComplexField
from kafman.core.schema.field.enum_field import EnumField
from kafman.core.schema.field.map_field import MapField
from kafman.core.schema.field.primitive_field import PrimitiveField
from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.schema_field_type import SchemaFieldType
from kafman.core.schema.schema_utils import SchemaUtils


class FieldFactory(ABC):

    @staticmethod
    def create_field(field: dict) -> 'SchemaField':
        """TODO"""
        field_name = SchemaUtils.check_and_get('name', field, True)
        field_type = SchemaUtils.check_and_get('type', field, True)
        field_doc = SchemaUtils.check_and_get('doc', field, False, f'the {field_name}')
        field_default = SchemaUtils.check_and_get('default', field, False, None)
        required = 'null' not in field_type
        avro_type = SchemaFieldType.of_type(field_type)
        if avro_type.is_complex():
            return ComplexField(field_name, field_doc, field_type, field_default, required)
        elif avro_type.is_primitive():
            return PrimitiveField(field_name, field_doc, avro_type, field_default, required)
        elif avro_type.is_enum():
            symbols = SchemaUtils.check_and_get('symbols', field, True)
            return EnumField(field_name, field_doc, symbols, field_default, required)
        elif avro_type.is_array():
            items = SchemaUtils.check_and_get('items', field, True)
            return ArrayField(field_name, field_doc, items, field_default, required)
        elif avro_type.is_map():
            values = SchemaUtils.check_and_get('values', field, True)
            return MapField(field_name, field_doc, values, field_default, required)
        else:
            raise InvalidStateError(f'Invalid field type: {avro_type}')

    @staticmethod
    def create_fields(fields: List[dict]) -> List[SchemaField]:
        """TODO"""
        record_fields = []
        for next_field in fields:
            field = FieldFactory.create_field(next_field)
            record_fields.append(field)

        return record_fields
