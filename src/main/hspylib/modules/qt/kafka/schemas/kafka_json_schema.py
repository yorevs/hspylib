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
from uuid import uuid4

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.serialization import StringSerializer

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import file_is_not_empty
from hspylib.core.tools.preconditions import check_state


class KafkaJsonSchema:
    """Json schema serializer/deserializer
       documentation: https://json-schema.org/
    """

    @staticmethod
    def extensions() -> List[str]:
        return ['*.json']

    @staticmethod
    def supports(file_extension: str) -> bool:
        """TODO"""
        return f"*{file_extension}" in KafkaJsonSchema.extensions()

    @staticmethod
    def to_dict(obj, ctx) -> dict:
        """TODO"""
        # fixme: implement
        return {}

    def __init__(self, filepath: str, charset: Charset = Charset.ISO8859_1):
        self._filepath = filepath
        check_state(file_is_not_empty(filepath))
        with open(filepath, 'r') as f_schema:
            schema_content = f_schema.read()
            self._content = defaultdict(None, json.loads(schema_content))
            self._type = self._content['type']
            self._schema = self._content['$schema']
            self._title = self._content['title']
            self._properties = self._content['properties']
            self._charset = charset
            schema_registry_conf = {'url': 'https://json-schema.org'}
            schema_registry_client = SchemaRegistryClient(schema_registry_conf)
            self._serializer = JSONSerializer(schema_content, schema_registry_client, self.to_dict)

    def schema_settings(self) -> dict:
        """TODO"""
        return {
            'key.serializer': StringSerializer(self._charset.value),
            'value.serializer': self._serializer
        }

    def key(self) -> str:
        """TODO"""
        return str(uuid4())

    def __str__(self):
        return f"type={self._type},  schema={self._schema},  title={self._title},  properties={len(self._properties)}"

    def __repr__(self):
        return str(self)

    def get_charset(self) -> str:
        return self._charset.value

    def get_field_names(self) -> List[str]:
        # fixme: implement
        return []

    def get_field_types(self) -> List[str]:
        # fixme: implement
        return []

    def get_content(self) -> str:
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
