#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: kafka_avro_schema.py
   @created: Sat, 17 Jul 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from typing import List

from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
from confluent_kafka.serialization import StringSerializer, StringDeserializer

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import get_by_key_or_default
from hspylib.core.tools.preconditions import check_not_none
from hspylib.modules.qt.kafka.consumer_config import ConsumerConfig
from hspylib.modules.qt.kafka.producer_config import ProducerConfig
from hspylib.modules.qt.kafka.schemas.kafka_schema import KafkaSchema
from hspylib.modules.qt.kafka.schemas.schema_field import SchemaField


class KafkaAvroSchema(KafkaSchema):
    """Apache AVRO schema serializer/deserializer
       Documentation: https://avro.apache.org/docs/current/gettingstartedpython.html
       Additional Ref: https://docs.confluent.io/5.3.0/schema-registry/serializer-formatter.html
    """

    @classmethod
    def extensions(cls) -> List[str]:
        return ['*.avsc']

    def __init__(
        self,
        filepath: str = None,
        registry_url: str = None,
        charset: Charset = Charset.ISO8859_1):

        super().__init__('AVRO', filepath, registry_url, charset)

    def _init_schema(self) -> None:
        self._type = check_not_none(self._content['type'])
        self._name = check_not_none(self._content['name'])
        fields = check_not_none(self._content['fields'])
        self._fields = [
            SchemaField.of_dict(
                f, bool(
                    next((t for t in f['type'] if isinstance(f['type'], list) and 'null' in f['type']), None) is None
                )
            ) for f in fields
        ]
        self._namespace = get_by_key_or_default(self._content, 'namespace', '')
        self._doc = get_by_key_or_default(self._content, 'doc', '')

    def serializer_settings(self) -> dict:
        return {
            ProducerConfig.KEY_SERIALIZER: StringSerializer(self._charset.value),
            ProducerConfig.VALUE_SERIALIZER: AvroSerializer(self._schema_client, self._schema_str, self.to_dict)
        }

    def deserializer_settings(self) -> dict:
        return {
            ConsumerConfig.KEY_DESERIALIZER: StringDeserializer(self._charset.value),
            ConsumerConfig.VALUE_DESERIALIZER: AvroDeserializer(self._schema_client, self._schema_str, self.from_dict)
        }
