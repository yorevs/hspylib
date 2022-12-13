#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: json_schema.py
   @created: Sun, 18 Jul 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from confluent_kafka.serialization import SerializationContext, StringDeserializer, StringSerializer
from hspylib.core.enums.charset import Charset
from hspylib.core.namespace import Namespace
from kafman.core.schema.kafka_schema import KafkaSchema
from kafman.core.schema.schema_type import SchemaType


class PlainSchema(KafkaSchema):
    """String schema serializer/deserializer"""

    @classmethod
    def to_dict(cls, obj: str, ctx: SerializationContext) -> dict:
        return {}

    @classmethod
    def from_dict(cls, obj: dict, ctx: SerializationContext) -> str:
        return str(Namespace("PlainSchemaObject"))

    def __init__(self, charset: Charset = Charset.UTF_8):
        super().__init__(SchemaType.PLAIN, charset=charset)

    def __str__(self):
        return f"[{self._schema_type}] type=plaintext"

    def _parse(self) -> None:
        pass

    def settings(self) -> dict:
        return {
            "key.serializer": StringSerializer(str(self._charset)),
            "value.serializer": StringSerializer(str(self._charset)),
            "key.deserializer": StringDeserializer(str(self._charset)),
            "value.deserializer": StringDeserializer(str(self._charset)),
        }
