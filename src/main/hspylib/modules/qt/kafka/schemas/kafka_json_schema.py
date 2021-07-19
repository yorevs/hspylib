#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: kafka_json_schema.py
   @created: Sun, 18 Jul 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import json
from collections import defaultdict
from typing import List, Any

from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.schema_registry.json_schema import JSONSerializer, JSONDeserializer
from confluent_kafka.serialization import StringSerializer, StringDeserializer, SerializationContext

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import file_is_not_empty
from hspylib.core.tools.preconditions import check_state
from hspylib.modules.qt.kafka.ConsumerConfig import ConsumerConfig
from hspylib.modules.qt.kafka.ProducerConfig import ProducerConfig
from hspylib.modules.qt.kafka.schemas.kafka_schema import KafkaSchema


class KafkaJsonSchema(KafkaSchema):
    """Json schema serializer/deserializer
       documentation: https://json-schema.org/
    """

    @classmethod
    def extensions(cls) -> List[str]:
        return ['*.json']

    @classmethod
    def supports(cls, file_extension: str) -> bool:
        """TODO"""
        return f"*{file_extension}" in KafkaJsonSchema.extensions()

    @classmethod
    def to_dict(cls, obj: str, ctx: SerializationContext) -> dict:
        """TODO"""
        return json.loads(obj)

    @classmethod
    def from_dict(cls, obj: dict, ctx: SerializationContext) -> str:
        """TODO"""
        return json.dumps(obj)

    def __init__(self, filepath: str, charset: Charset = Charset.ISO8859_1):
        super().__init__(filepath, charset)
        check_state(file_is_not_empty(filepath))
        with open(filepath, 'r') as f_schema:
            self._schema_str = f_schema.read()
            self._content = defaultdict(None, json.loads(self._schema_str))
            self._type = self._content['type']
            self._schema = self._content['$schema']
            self._title = self._content['title']
            self._description = self._content['description']
            self._properties = self._content['properties']
            self._schema_conf = {'url': 'http://localhost:8081'}
            self._schema_client = SchemaRegistryClient(self._schema_conf)
            json_schema = Schema(self._schema_str, 'JSON')
            self._schema_id = self._schema_client.register_schema(self._title.lower(), json_schema)

    def serializer_settings(self) -> dict:
        """TODO"""
        return {
            ProducerConfig.KEY_SERIALIZER: StringSerializer(self._charset.value),
            ProducerConfig.VALUE_SERIALIZER: JSONSerializer(self._schema_str, self._schema_client, self.to_dict)
        }

    def deserializer_settings(self) -> dict:
        """TODO"""
        return {
            ConsumerConfig.KEY_DESERIALIZER: StringDeserializer(self._charset.value),
            ConsumerConfig.VALUE_DESERIALIZER: JSONDeserializer(self._schema_str, self.from_dict)
        }

    def __str__(self):
        return f"[JSON] title={self._title}, type={self._type}, schema={self._schema}"

    def get_charset(self) -> str:
        return self._charset.value

    def get_field_names(self) -> List[str]:
        return [f for f in self._properties.keys()]

    def get_field_types(self) -> List[str]:
        return [f['type'] for f in self._properties.values()]

    def get_content(self) -> defaultdict:
        return self._content

    def get_filepath(self) -> str:
        return self._filepath

    def get_type(self) -> str:
        return self._type

    def get_schema(self) -> str:
        return self._schema

    def get_title(self) -> str:
        return self._title

    def get_properties(self) -> List[Any]:
        return self._properties
