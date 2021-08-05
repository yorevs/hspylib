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

from confluent_kafka.serialization import StringSerializer, StringDeserializer, SerializationContext

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import new_dynamic_object
from kafman.src.main.core.kafka.schemas.kafka_schema import KafkaSchema


class KafkaPlainSchema(KafkaSchema):
    """String schema serializer/deserializer"""

    @classmethod
    def to_dict(cls, obj: str, ctx: SerializationContext) -> dict:
        return {}

    @classmethod
    def from_dict(cls, obj: dict, ctx: SerializationContext) -> str:
        return str(new_dynamic_object('PlainSchemaObject'))

    def __init__(self, charset: Charset = Charset.ISO8859_1):
        super().__init__(schema_type='PLAIN', charset=charset)

    def __str__(self):
        return f"[{self._schema_type}] type=plaintext"

    def _init_schema(self) -> None:
        pass

    def serializer_settings(self) -> dict:
        """TODO"""
        return {
            'key.serializer': StringSerializer(self._charset.value),
            'value.serializer': StringSerializer(self._charset.value)
        }

    def deserializer_settings(self) -> dict:
        """TODO"""
        return {
            'key.deserializer': StringDeserializer(self._charset.value),
            'value.deserializer': StringDeserializer(self._charset.value)
        }
