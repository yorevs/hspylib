#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: json_schema.py
   @created: Sun, 18 Jul 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from os import path
from typing import List

from confluent_kafka.schema_registry.json_schema import JSONDeserializer, JSONSerializer
from confluent_kafka.serialization import StringDeserializer, StringSerializer
from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import SchemaRegistryError
from hspylib.core.tools.commons import get_by_key_or_default
from kafman.core.consumer_config import ConsumerConfig
from kafman.core.producer_config import ProducerConfig
from kafman.core.schema.kafka_schema import KafkaSchema
from kafman.core.schema.schema_field import SchemaField


class JsonSchema(KafkaSchema):
    """Json schema serializer/deserializer
       Documentation: https://json-schema.org/
       Additional Ref: https://docs.confluent.io/5.3.0/schema-registry/serializer-formatter.html
    """

    DEFAULT_NAMESPACE = 'http://json-schema.org/draft-04/schema#'

    @classmethod
    def extensions(cls) -> List[str]:
        return ['*.json']

    @classmethod
    def get_items(cls, field_attrs: dict) -> List[str]:
        """Return the schema items from the loaded attributes"""
        items = get_by_key_or_default(field_attrs, 'items')
        if isinstance(items, list):
            return items
        if isinstance(items, dict):
            return get_by_key_or_default(items, 'enum', [])

        return []

    def __init__(
        self,
        filepath: str = None,
        registry_url: str = None,
        charset: Charset = Charset.ISO8859_1):

        super().__init__('JSON', filepath, registry_url, charset)

    def is_required(self, key: str) -> bool:
        """Check if the field represented by 'key' is required"""
        required_list = get_by_key_or_default(self._content, 'required', [])
        return key in required_list

    def serializer_settings(self) -> dict:
        return {
            ProducerConfig.KEY_SERIALIZER: StringSerializer(self._charset.value),
            ProducerConfig.VALUE_SERIALIZER: JSONSerializer(self._schema_str, self._schema_client, self.to_dict)
        }

    def deserializer_settings(self) -> dict:
        return {
            ConsumerConfig.KEY_DESERIALIZER: StringDeserializer(self._charset.value),
            ConsumerConfig.VALUE_DESERIALIZER: JSONDeserializer(self._schema_str, self.from_dict)
        }

    def _parse(self) -> None:
        self._name = self._name = get_by_key_or_default(
            self._content, 'title', path.basename(path.splitext(self._filepath)[0]))
        self._type = self._type = get_by_key_or_default(self._content, 'type', 'object')
        self._fields = self._get_fields()
        self._doc = get_by_key_or_default(self._content, 'description', 'no-description')
        self._namespace = get_by_key_or_default(self._content, '$schema', self.DEFAULT_NAMESPACE)

    def _get_fields(self) -> List[SchemaField]:
        """Return the list of schema fields based on the root element type"""
        if self._type == 'object':
            fields = get_by_key_or_default(self._content, 'properties', {})
            if not fields:
                fields = self._content
        elif self._type == 'array':
            items = get_by_key_or_default(self._content, 'items')
            fields = get_by_key_or_default(items if items else self._content, 'properties', {})
            if not fields:
                fields = self._content
        else:
            raise SchemaRegistryError(f"Invalid field type: {self._type}")

        return [
            SchemaField.of(
                self, key,
                f['type'] if 'type' in f else 'object', f,
                self.is_required(key)) for key, f in fields.items()
        ]
