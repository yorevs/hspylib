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
from os import path
from typing import List

from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.serialization import StringDeserializer, StringSerializer
from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import get_by_key_or_default, search_dict
from kafman.core.consumer_config import ConsumerConfig
from kafman.core.producer_config import ProducerConfig
from kafman.core.schema.kafka_schema import KafkaSchema
from kafman.core.schema.schema_field import SchemaField


class AvroSchema(KafkaSchema):
    """Apache AVRO schema serializer/deserializer
       Documentation: https://avro.apache.org/docs/current/gettingstartedpython.html
       Additional Ref: https://docs.confluent.io/5.3.0/schema-registry/serializer-formatter.html
    """

    @classmethod
    def extensions(cls) -> List[str]:
        return ['*.avsc']

    @classmethod
    def get_items(cls, field_attrs: dict) -> List[str]:
        found, symbols = search_dict(field_attrs, 'type.symbols')
        if found and isinstance(symbols, list):
            return symbols

        return []

    @classmethod
    def is_required(cls, field: dict) -> bool:
        """Check if the field is required"""
        return bool(next(
            (t for t in field['type'] if isinstance(field['type'], list) and 'null' in field['type']), None) is None)

    @classmethod
    def find_type(cls, field: dict) -> str:
        """Return the field type"""
        return next((ft['type'] for ft in field['type'] if isinstance(ft, dict)), None) \
            if isinstance(field['type'], list) \
            else field['type']

    def __init__(
        self,
        filepath: str = None,
        registry_url: str = None,
        charset: Charset = Charset.ISO8859_1):
        super().__init__('AVRO', filepath, registry_url, charset)

    def _parse(self) -> None:
        """TODO"""
        self._name = get_by_key_or_default(
            self._content, 'name', path.basename(path.splitext(self._filepath)[0]))
        self._type = get_by_key_or_default(self._content, 'type', 'record')
        fields = get_by_key_or_default(self._content, 'fields', [])
        self._fields = [
            SchemaField.of(self, f['name'], self.find_type(f), f, self.is_required(f)) for f in fields
        ]
        self._namespace = get_by_key_or_default(self._content, 'namespace', '')
        self._doc = get_by_key_or_default(self._content, 'doc', '')

    def serializer_settings(self) -> dict:
        """TODO"""
        return {
            ProducerConfig.KEY_SERIALIZER: StringSerializer(self._charset.value),
            ProducerConfig.VALUE_SERIALIZER: AvroSerializer(self._schema_client, self._schema_str, self.to_dict)
        }

    def deserializer_settings(self) -> dict:
        """TODO"""
        return {
            ConsumerConfig.KEY_DESERIALIZER: StringDeserializer(self._charset.value),
            ConsumerConfig.VALUE_DESERIALIZER: AvroDeserializer(self._schema_client, self._schema_str, self.from_dict)
        }
