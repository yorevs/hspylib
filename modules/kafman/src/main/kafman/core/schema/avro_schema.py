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
from typing import List

from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.serialization import StringDeserializer, StringSerializer
from hspylib.core.enums.charset import Charset
from hspylib.core.enums.enumeration import Enumeration

from kafman.core.consumer_config import ConsumerConfig
from kafman.core.producer_config import ProducerConfig
from kafman.core.schema.kafka_schema import KafkaSchema
from kafman.core.schema.schema_type import SchemaType


class _AvroType(Enumeration):
    """TODO"""

    # @formatter:off
    NULL            = 'null'
    BOOLEAN         = 'boolean'
    INT             = 'int'
    LONG            = 'long'
    FLOAT           = 'float'
    DOUBLE          = 'double'
    BYTES           = 'bytes'
    STRING          = 'string'
    RECORD          = 'record'
    ENUM            = 'enum'
    ARRAY           = 'array'
    MAP             = 'map'
    FIXED           = 'fixed'
    # @formatter:on


class AvroSchema(KafkaSchema):
    """Apache AVRO schema serializer/deserializer
       Documentation: https://avro.apache.org/docs/current/gettingstartedpython.html
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

    def _parse(self) -> None:
        """TODO"""
        if self._content_text.startswith('{') and self._content_text.endswith('}'):
            # Defined type or record
            pass
        elif self._content_text.startswith('[') and self._content_text.endswith(']'):
            # Array
            pass

    def settings(self) -> dict:
        """TODO"""
        return {
            ProducerConfig.KEY_SERIALIZER: StringSerializer(self._charset.value),
            ProducerConfig.VALUE_SERIALIZER: AvroSerializer(self._schema_client, self._content_text, self.to_dict),
            ConsumerConfig.KEY_DESERIALIZER: StringDeserializer(self._charset.value),
            ConsumerConfig.VALUE_DESERIALIZER: AvroDeserializer(self._schema_client, self._content_text, self.from_dict)
        }
