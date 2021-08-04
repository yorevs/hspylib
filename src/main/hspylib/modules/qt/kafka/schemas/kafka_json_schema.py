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
from typing import List

from confluent_kafka.schema_registry.json_schema import JSONSerializer, JSONDeserializer
from confluent_kafka.serialization import StringSerializer, StringDeserializer
from hspylib.core.tools.preconditions import check_not_none

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import get_by_key_or_default
from hspylib.modules.qt.kafka.consumer_config import ConsumerConfig
from hspylib.modules.qt.kafka.producer_config import ProducerConfig
from hspylib.modules.qt.kafka.schemas.kafka_schema import KafkaSchema
from hspylib.modules.qt.kafka.schemas.schema_field import SchemaField


class KafkaJsonSchema(KafkaSchema):
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

    def _init_schema(self) -> None:
        self._type = check_not_none(self._content['type'])
        self._name = check_not_none(self._content['title'])
        fields = check_not_none(self._content['properties'])
        check_not_none(fields)
        self._fields = [SchemaField.of_map(self, key, f, self.is_required(key)) for key, f in fields.items()]
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
