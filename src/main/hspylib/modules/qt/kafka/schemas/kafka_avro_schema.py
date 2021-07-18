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
import json
from collections import defaultdict
from typing import Any, List

from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
from confluent_kafka.serialization import StringSerializer, StringDeserializer

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import file_is_not_empty
from hspylib.core.tools.preconditions import check_state
from hspylib.modules.qt.kafka.schemas.kafka_schema import KafkaSchema


class KafkaAvroSchema(KafkaSchema):
    """Apache AVRO schema serializer/deserializer
       documentation: https://avro.apache.org/docs/current/gettingstartedpython.html
    """

    @classmethod
    def extensions(cls) -> List[str]:
        return ['*.avsc']

    @classmethod
    def supports(cls, file_extension: str) -> bool:
        """TODO"""
        return f"*{file_extension}" in KafkaAvroSchema.extensions()

    def __init__(self, filepath: str, charset: Charset = Charset.ISO8859_1):
        super().__init__(filepath, charset)
        check_state(file_is_not_empty(filepath))
        with open(filepath, 'r') as f_schema:
            self._schema_str = f_schema.read()
            self._content = defaultdict(None, json.loads(self._schema_str))
            self._type = self._content['type']
            self._namespace = self._content['namespace']
            self._name = self._content['name']
            self._fields = self._content['fields']

    def __str__(self):
        return f"type={self._type},  namespace={self._namespace},  name={self._name},  fields={len(self._fields)}"

    def __repr__(self):
        return str(self)

    def serializer_settings(self) -> dict:
        """TODO"""
        return {
            'key.serializer': StringSerializer(self._charset.value),
            'value.serializer': AvroSerializer(self._schema_str, self._schema_str, self.to_dict)
        }

    def deserializer_settings(self) -> dict:
        """TODO"""
        return {
            'key.deserializer': StringDeserializer(self._charset.value),
            'value.deserializer': AvroDeserializer(self._schema_str, self._schema_str, self.from_dict)
        }

    def get_field_names(self) -> List[str]:
        return [f['name'] for f in self._fields]

    def get_field_types(self) -> List[str]:
        return [f['type'] for f in self._fields]

    def get_content(self) -> defaultdict:
        return self._content

    def get_type(self) -> str:
        return self._type

    def get_namespace(self) -> str:
        return self._namespace

    def get_name(self) -> str:
        return self._name

    def get_fields(self) -> List[Any]:
        return self._fields
