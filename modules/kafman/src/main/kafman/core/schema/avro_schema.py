#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: avro_schema.py
   @created: Sat, 17 Jul 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from collections import defaultdict
from typing import List, Tuple

from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.serialization import StringDeserializer, StringSerializer
from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import InvalidStateError
from hspylib.modules.qt.promotions.hstacked_widget import HStackedWidget
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from kafman.core.consumer_config import ConsumerConfig
from kafman.core.producer_config import ProducerConfig
from kafman.core.schema.field.field_factory import FieldFactory
from kafman.core.schema.field.record_field import RecordField
from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.kafka_schema import KafkaSchema
from kafman.core.schema.schema_type import SchemaType
from kafman.core.schema.schema_utils import SchemaUtils
from kafman.core.schema.widget_utils import WidgetUtils


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
        return ['*.avsc']

    def __init__(
        self,
        filepath: str,
        registry_url: str,
        charset: Charset = Charset.UTF_8):
        super().__init__(SchemaType.AVRO, filepath, registry_url, charset)

    def settings(self) -> dict:
        """TODO"""
        return {
            ProducerConfig.KEY_SERIALIZER: StringSerializer(self._charset.value),
            ProducerConfig.VALUE_SERIALIZER: AvroSerializer(self._schema_client, self._content_text, self.to_dict),
            ConsumerConfig.KEY_DESERIALIZER: StringDeserializer(self._charset.value),
            ConsumerConfig.VALUE_DESERIALIZER: AvroDeserializer(self._schema_client, self._content_text, self.from_dict)
        }

    def create_schema_form_row_widget(self, field: SchemaField) -> Tuple[QLabel, QLabel, QWidget]:

        label = QLabel(f"{field.name[0].upper() + field.name[1:]}: ")
        if field.required:
            req_label = QLabel('*')
            req_label.setStyleSheet('QLabel {color: #FF554D;}')
        else:
            req_label = QLabel(' ')
        req_label.setToolTip(f"This field is {'required' if field.required else 'optional'}")
        widget = field.create_input_widget()

        return req_label, label, widget

    def create_schema_form_widget(
        self, form_stack: HStackedWidget, parent_pane: QFrame = None, fields: List[SchemaField] = None) -> int:

        form_fields = fields if fields is not None else self._attributes.fields
        form_pane = QFrame(form_stack)

        if not form_fields or len(form_fields) <= 0:
            layout = QVBoxLayout(form_pane)
            label = QLabel(f'Unable to detect valid fields')
            label.setStyleSheet('QLabel {color: #FF554D;}')
            layout.addWidget(label)
            form_pane.setLayout(layout)
            form_pane.resize(600, 400)
            return 0

        layout = QGridLayout(form_pane)
        form_pane.setLayout(layout)
        index = form_stack.addWidget(form_pane)
        form_pane.setObjectName(f"Form {str(index)}")
        row = None

        for row, field in enumerate(form_fields):
            req_label, label, widget = self.create_schema_form_row_widget(field)
            layout.addWidget(label, row, 0)
            layout.addWidget(req_label, row, 1)
            if isinstance(field, RecordField):
                record_fields = FieldFactory.create_fields(field.fields)
                child_index = self.create_schema_form_widget(form_stack, form_pane, record_fields)
                widget = WidgetUtils.create_goto_form_button(child_index, form_stack)
            if widget is not None:
                layout.addWidget(widget, row, 2)

        if index > 0:
            parent_index = form_stack.indexOf(parent_pane)
            button_back = WidgetUtils.create_back_button(parent_index, form_stack)
            layout.addWidget(button_back, row + 1, 0)

        return index

    def _parse(self) -> None:

        if not self._content_text.startswith('{') or not  self._content_text.endswith('}'):
            raise InvalidStateError(f"UnsupportedSchema: {self._filepath}")

        self._schema_name = SchemaUtils.check_and_get('name', self._content_dict)
        self._attributes.name = self._schema_name
        self._attributes.namespace = SchemaUtils.check_and_get(
            'namespace', self._content_dict, required=False)
        self._attributes.doc = SchemaUtils.check_and_get(
            'doc', self._content_dict, required=False, default=f'the {self._schema_name}')
        self._attributes.aliases = SchemaUtils.check_and_get(
            'aliases', self._content_dict, required=False)

        field_type = SchemaUtils.check_and_get('type', self._content_dict)
        if 'record' == field_type:
            fields = SchemaUtils.check_and_get('fields', self._content_dict)
            self._attributes.fields = FieldFactory.create_fields(fields)

    def form_object(self) -> dict:

        dict_fields = defaultdict()
        for field in self._attributes.fields:
            dict_fields.update({field.name: field.a_type.empty_value()})

        return dict_fields
