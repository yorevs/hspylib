#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: avro_schema.py
   @created: Sat, 17 Jul 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.serialization import StringDeserializer, StringSerializer
from fastavro.validation import validate as validate_schema
from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import InvalidStateError
from hspylib.core.preconditions import check_not_none
from hspylib.modules.qt.promotions.hstacked_widget import HStackedWidget
from kafman.core.consumer.consumer_config import ConsumerConfig
from kafman.core.producer.producer_config import ProducerConfig
from kafman.core.schema.avro.field.field_factory import FieldFactory
from kafman.core.schema.avro.field.record_field import RecordField
from kafman.core.schema.kafka_schema import KafkaSchema
from kafman.core.schema.schema_field import SchemaField
from kafman.core.schema.schema_type import SchemaType
from kafman.views.promotions.form_pane import FormPane
from typing import List

import avro.schema as schema_parser


class AvroSchema(KafkaSchema):
    """Apache AVRO schema serializer/deserializer
    Documentation:
     - https://avro.apache.org/docs/current/spec.html
     - https://avro.apache.org/docs/current/gettingstartedpython.html
    Additional Ref: https://docs.confluent.io/5.3.0/schema-registry/serializer-formatter.html

     E.g:.
     {
       "type": "record",
       "name": "myRecord",
       "fields": [
           {"name": "name",  "type": "string" }
         , {"name": "calories", "type": "float" }
         , {"name": "colour", "type": "string" }
       ]
     }
    """

    @classmethod
    def extensions(cls) -> List[str]:
        return ["*.avsc"]

    def __init__(self, filepath: str, registry_url: str, charset: Charset = Charset.UTF_8):
        super().__init__(SchemaType.AVRO, filepath, registry_url, charset)

    def settings(self) -> dict:
        """TODO"""
        return {
            ProducerConfig.KEY_SERIALIZER: StringSerializer(self._charset.value),
            ProducerConfig.VALUE_SERIALIZER: AvroSerializer(self._schema_client, self._content_text, self.to_dict),
            ConsumerConfig.KEY_DESERIALIZER: StringDeserializer(self._charset.value),
            ConsumerConfig.VALUE_DESERIALIZER: AvroDeserializer(
                self._schema_client, self._content_text, self.from_dict
            ),
        }

    def validate(self, json_form: dict) -> None:
        validate_schema(json_form, self.get_content_dict())

    def create_schema_form_widget(
        self,
        form_stack: HStackedWidget,
        parent_pane: FormPane = None,
        form_name: str = None,
        fields: List[SchemaField] = None,
    ) -> int:
        """Create the stacked frame with the form widget"""

        form_fields = fields if fields is not None else self._attributes.fields

        if not form_fields or len(form_fields) <= 0:
            return 0

        form_name = form_name if form_name is not None else self._schema_name
        form_pane = FormPane(form_stack, parent_pane, form_name)
        index = form_stack.addWidget(form_pane)

        for row, field in enumerate(form_fields):
            check_not_none(field)
            req_label, label, widget = KafkaSchema.create_schema_form_row_widget(field)
            if isinstance(field, RecordField):
                record_fields = FieldFactory.create_schema_fields(field.fields)
                child_index = self.create_schema_form_widget(form_stack, form_pane, field.name, record_fields)
                form_pane.add_form_button(field.name, label, req_label, row, child_index, form_stack)
            else:
                form_pane.add_field(field.name, label, req_label, widget, row)

        if index > 0:
            parent_index = form_stack.indexOf(parent_pane)
            form_pane.add_back_button(parent_index, form_stack)

        return index

    def _parse(self) -> None:

        self._parsed = schema_parser.parse(self._content_text)

        self._schema_name = self._parsed.name
        self._attributes.name = self._parsed.fullname
        self._attributes.namespace = self._parsed.namespace
        self._attributes.doc = self._parsed.doc

        field_type = self._parsed.type

        if "record" == field_type:
            self._attributes.fields = FieldFactory.create_schema_fields(self._parsed.fields)
        else:
            # TODO Check if it is needed to add the other types such as array, map, etc...
            raise InvalidStateError(f"Unsupported field type {field_type}")
