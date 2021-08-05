#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: json_schema.py
   @created: Sun, 18 Jul 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import os.path as path
from typing import List

from confluent_kafka.schema_registry.json_schema import JSONSerializer, JSONDeserializer
from confluent_kafka.serialization import StringSerializer, StringDeserializer

from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import SchemaRegistryError
from hspylib.core.tools.commons import get_by_key_or_default
from kafman.src.main.core.consumer_config import ConsumerConfig
from kafman.src.main.core.producer_config import ProducerConfig
from kafman.src.main.core.schema.kafka_schema import KafkaSchema
from kafman.src.main.core.schema.registry_field import RegistryField


class JsonSchema(KafkaSchema):
    """Json schema serializer/deserializer
       Documentation: https://json-schema.org/
       Additional Ref: https://docs.confluent.io/5.3.0/schema-registry/serializer-formatter.html
    """

    @classmethod
    def extensions(cls) -> List[str]:
        return ['*.json']

    @classmethod
    def array_items(cls, field_attrs: dict) -> List[str]:
        """TODO"""
        items = get_by_key_or_default(field_attrs, 'items')
        if isinstance(items, list):
            return items
        elif isinstance(items, dict):
            return get_by_key_or_default(items, 'enum', [])

        return []

    def __init__(
        self,
        filepath: str = None,
        registry_url: str = None,
        charset: Charset = Charset.ISO8859_1):

        super().__init__('JSON', filepath, registry_url, charset)

    def is_required(self, key: str) -> bool:
        """TODO"""
        required_list = get_by_key_or_default(self._content, 'required', [])
        return key in required_list

    def _parse(self) -> None:
        self._name = self._name = get_by_key_or_default(
            self._content, 'title', path.basename(path.splitext(self._filepath)[0]))
        self._type = self._type = get_by_key_or_default(self._content, 'type', 'object')
        self._fields = self._parse_fields()
        self._doc = get_by_key_or_default(self._content, 'description', '')
        self._namespace = get_by_key_or_default(self._content, '$schema', '')

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

    def _parse_fields(self) -> List[RegistryField]:
        """TODO"""
        if self._type == 'object':
            fields = get_by_key_or_default(self._content, 'properties', {})
        elif self._type == 'array':
            items = get_by_key_or_default(self._content, 'items')
            fields = get_by_key_or_default(items if items else self._content, 'properties', {})
        else:
            raise SchemaRegistryError(f"Invalid field type: {self._type}")

        return [
            RegistryField.of(self, key, f['type'], f, self.is_required(key)) for key, f in fields.items()
        ]
