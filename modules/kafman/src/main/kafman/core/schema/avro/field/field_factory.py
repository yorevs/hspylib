#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Kafman
   @package: kafman.core.schema.avro.field
      @file: field_factory.py
   @created: Wed, 1 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from abc import ABC
from avro.schema import ArraySchema, EnumSchema, Field, MapSchema, PrimitiveSchema, RecordSchema, Schema, UnionSchema
from hspylib.core.exception.exceptions import InvalidStateError
from hspylib.core.preconditions import check_not_none
from kafman.core.schema.avro.avro_type import AvroType
from kafman.core.schema.avro.field.array_field import ArrayField
from kafman.core.schema.avro.field.enum_field import EnumField
from kafman.core.schema.avro.field.map_field import MapField
from kafman.core.schema.avro.field.primitive_field import PrimitiveField
from kafman.core.schema.avro.field.record_field import RecordField
from kafman.core.schema.schema_field import SchemaField
from typing import List, Optional, Tuple


class FieldFactory(ABC):
    @staticmethod
    def create_field(field: Field) -> "SchemaField":
        """TODO"""
        field_name, field_type = field.name, field.type
        field_doc = field.doc or f"the {field_name}"
        field_default = field.default if field.has_default else None
        required = FieldFactory.is_required(field)
        avro_type = AvroType.of_type(field_type)
        if avro_type.is_primitive():
            schema_field = PrimitiveField(field_name, field_doc, avro_type, field_default, required)
        else:
            complex_type = FieldFactory._get_union_type(field_type) if avro_type.is_union() else field_type
            if isinstance(complex_type, PrimitiveSchema):
                a_type = AvroType.of_value(complex_type.type)
                schema_field = PrimitiveField(field_name, field_doc, a_type, field_default, required)
            elif isinstance(complex_type, EnumSchema):
                schema_field = EnumField(field_name, field_doc, complex_type.symbols, field_default, required)
            elif isinstance(complex_type, ArraySchema):
                schema_field = ArrayField(field_name, field_doc, complex_type.items, field_default, required)
            elif isinstance(complex_type, MapSchema):
                schema_field = MapField(field_name, field_doc, complex_type.values, field_default, required)
            elif isinstance(complex_type, RecordSchema):
                schema_field = RecordField(field_name, field_doc, complex_type.fields, required)
            else:
                schema_field = InvalidStateError(f"Invalid field type: {complex_type}")

        check_not_none(schema_field, f"Unable to parse field {field_name}")

        return schema_field

    @staticmethod
    def _get_union_type(union_type: UnionSchema) -> Optional[Schema]:
        return next(
            (sch for sch in union_type.schemas if not isinstance(sch, PrimitiveSchema) or sch.fullname != "null"), None
        )

    @staticmethod
    def create_schema_fields(fields: Tuple[Field]) -> List[SchemaField]:
        """TODO"""
        record_fields = []
        for next_field in fields:
            field = FieldFactory.create_field(next_field)
            record_fields.append(field)

        return record_fields

    @staticmethod
    def is_required(field: Field) -> bool:
        if isinstance(field.type, UnionSchema):
            has_null = next((sch for sch in field.type.schemas if sch.fullname == "null"), None)
            return has_null is None

        return True
