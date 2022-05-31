from abc import ABC
from typing import List, Union

from hspylib.core.exception.exceptions import InvalidStateError

from kafman.core.schema.field.array_field import ArrayField
from kafman.core.schema.field.enum_field import EnumField
from kafman.core.schema.field.map_field import MapField
from kafman.core.schema.field.primitive_field import PrimitiveField
from kafman.core.schema.field.record_field import RecordField
from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.field.schema_field_type import SchemaFieldType
from kafman.core.schema.schema_utils import SchemaUtils


class FieldFactory(ABC):

    @staticmethod
    def create_field(field: dict) -> 'SchemaField':
        """TODO"""
        field_name = SchemaUtils.check_and_get('name', field)
        field_type = SchemaUtils.check_and_get('type', field)
        field_doc = SchemaUtils.check_and_get('doc', field, False, f'the {field_name}')
        field_default = SchemaUtils.check_and_get('default', field, False)
        required = 'null' not in field_type
        avro_type = SchemaFieldType.of_type(field_type)
        if avro_type.is_primitive():
            return PrimitiveField(field_name, field_doc, avro_type, field_default, required)
        else:
            complex_type = FieldFactory._get_field_type(field)
            if avro_type.is_enum():
                symbols = SchemaUtils.check_and_get('symbols', complex_type)
                return EnumField(field_name, field_doc, symbols, field_default, required)
            elif avro_type.is_array():
                items = SchemaUtils.check_and_get('items', complex_type)
                return ArrayField(field_name, field_doc, items, field_default, required)
            elif avro_type.is_map():
                values = SchemaUtils.check_and_get('values', complex_type)
                return MapField(field_name, field_doc, values, field_default, required)
            elif avro_type.is_record():
                fields = SchemaUtils.check_and_get('fields', complex_type)
                return RecordField(field_name, field_doc, fields, required)
            else:
                raise InvalidStateError(f'Invalid field type: {avro_type}')

    @staticmethod
    def _get_field_type(field: Union[dict, list]) -> Union[dict, list]:

        if isinstance(field, dict):
            ret_type = field['type']
        else:
            ret_type = next((f for f in field if f != 'null'), field)

        if isinstance(ret_type, str):
            raise InvalidStateError(f'Invalid field type: {field}')
        elif isinstance(ret_type, list):
            return next((f for f in ret_type if f != 'null'), field)

        return ret_type

    @staticmethod
    def create_fields(fields: List[dict]) -> List[SchemaField]:
        """TODO"""
        record_fields = []
        for next_field in fields:
            field = FieldFactory.create_field(next_field)
            record_fields.append(field)

        return record_fields
