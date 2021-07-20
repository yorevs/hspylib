#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: kafka_schema.py
   @created: Sum, 18 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import json
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Any
from uuid import uuid4

from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.serialization import SerializationContext

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import file_is_not_empty, build_url
from hspylib.core.tools.preconditions import check_state, check_not_none


class KafkaSchema(ABC):
    """String schema serializer/deserializer"""

    @classmethod
    def extensions(cls) -> List[str]:
        """TODO"""
        return []

    @classmethod
    def supports(cls, file_extension: str) -> bool:
        """TODO"""
        return f"*{file_extension}" in cls.extensions()

    @classmethod
    def to_dict(cls, obj: str, ctx: SerializationContext) -> dict:
        return json.loads(obj)

    @classmethod
    def from_dict(cls, obj: dict, ctx: SerializationContext) -> str:
        return json.dumps(obj)

    @classmethod
    def key(cls) -> str:
        """TODO"""
        return str(uuid4())

    def __init__(
        self,
        schema_type: str,
        filepath: str = None,
        registry_url: str = None,
        charset: Charset = Charset.ISO8859_1):

        self._filepath = filepath
        self._schema_type = schema_type
        self._charset = charset
        self._namespace = ''
        self._name = ''
        self._type = ''
        self._doc = ''
        self._fields = []

        if filepath:
            check_state(file_is_not_empty(filepath))
            with open(filepath, 'r') as f_schema:
                self._schema_str = f_schema.read()
                self._content = defaultdict(None, json.loads(self._schema_str))
                check_not_none(self._content)
            schema_conf = {'url': build_url(registry_url) or 'http://localhost:8081'}
            self._schema_client = SchemaRegistryClient(schema_conf)
            schema = Schema(self._schema_str, self._schema_type)
            self._init_schema()
            self._schema_id = self._schema_client.register_schema(self._name.lower(), schema)

    def __str__(self):
        return f"[{self._schema_type}] name={self._name}, type={self._type}, namespace={self._namespace}"

    def __repr__(self):
        return self._schema_type

    @abstractmethod
    def _init_schema(self) -> None:
        """TODO"""
        pass

    @abstractmethod
    def serializer_settings(self) -> dict:
        """TODO"""
        pass

    @abstractmethod
    def deserializer_settings(self) -> dict:
        """TODO"""
        pass

    def get_filepath(self) -> str:
        """TODO"""
        return self._filepath

    def get_charset(self) -> str:
        """TODO"""
        return self._charset.value

    def get_content(self) -> dict:
        """TODO"""
        return self._content

    def get_field_names(self) -> List[str]:
        """TODO"""
        return [f['name'] for f in self._fields]

    def get_field_types(self) -> List[str]:
        """TODO"""
        return [f['type'] for f in self._fields]

    def get_type(self) -> str:
        """TODO"""
        return self._type

    def get_namespace(self) -> str:
        return self._namespace

    def get_name(self) -> str:
        return self._name

    def get_fields(self) -> List[Any]:
        return self._fields
