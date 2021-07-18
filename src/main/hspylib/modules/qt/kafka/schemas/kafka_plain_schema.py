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
from collections import defaultdict
from typing import List

from confluent_kafka.serialization import StringSerializer, StringDeserializer

from hspylib.core.enums.charset import Charset
from hspylib.modules.qt.kafka.schemas.kafka_schema import KafkaSchema


class KafkaPlainSchema(KafkaSchema):
    """String schema serializer/deserializer"""

    def __init__(self, charset: Charset = Charset.ISO8859_1):
        super().__init__(charset=charset)

    def __str__(self):
        return f"name=StringSerializer,  type=plaintext"

    def __repr__(self):
        return str(self)

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

    def get_field_types(self) -> List[str]:
        pass

    def get_content(self) -> defaultdict:
        pass

    def get_type(self) -> str:
        pass

    def get_field_names(self) -> List[str]:
        pass
