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
import logging as log
from abc import ABC, abstractmethod
from collections import defaultdict
from json.decoder import JSONDecodeError
from typing import List, Optional
from uuid import uuid4

from confluent_kafka.schema_registry import SchemaRegistryClient, Schema, SchemaRegistryError
from confluent_kafka.serialization import SerializationContext
from requests.exceptions import ConnectTimeout, ConnectionError, InvalidURL, ReadTimeout

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import file_is_not_empty, build_url, syserr
from hspylib.core.tools.preconditions import check_state, check_not_none, check_argument
from hspylib.modules.qt.kafka.schemas.schema_field import SchemaField


class KafkaSchema(ABC):
    """String schema serializer/deserializer"""

    SUPPORTED_SCHEMA_TYPES = ["PLAIN", "AVRO", "JSON", "PROTOBUF"]

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

        check_argument(schema_type in self.SUPPORTED_SCHEMA_TYPES)
        self._filepath = filepath
        self._registry_url = registry_url
        self._schema_type = schema_type
        self._charset = charset
        self._schema_id = None
        self._namespace = None
        self._doc = None
        self._name = None
        self._type = None
        self._fields = None

        try:
            if filepath:
                check_state(file_is_not_empty(filepath), f"Schema file not found: {filepath}")
                with open(filepath, 'r') as f_schema:
                    self._schema_str = f_schema.read()
                    self._content = defaultdict(None, json.loads(self._schema_str))
                    check_not_none(self._content)
                self._schema_conf = {'url': build_url(self._registry_url) or 'http://localhost:8081'}
                self._schema_client = SchemaRegistryClient(self._schema_conf)
                self._schema = Schema(self._schema_str, self._schema_type)
                self._init_schema()
        except (KeyError, TypeError, JSONDecodeError) as err:
            syserr(f"Unable to load schema => {str(err)}")
            log.error(f"Unable to load schema => {str(err)}")

    def __getitem__(self, index: int):
        return self._fields[index]

    def register_schema(self) -> bool:
        """TODO"""
        try:
            self._schema_id = self._schema_client.register_schema(self._name, self._schema)
        except (AttributeError, ConnectTimeout, ConnectionError, ReadTimeout, InvalidURL, SchemaRegistryError) as err:
            syserr(f"Unable to register schema at: {self._registry_url} => {str(err)}")
            log.error(f"Unable to register schema at: {self._registry_url} => {str(err)}")
            return False
        log.info(f"Schema successfully registered id={self._schema_id} at {self._registry_url}")
        return True

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

    def get_schema_type(self) -> str:
        """TODO"""
        return self._schema_type

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
        return [f.get_name() for f in self._fields]

    def get_field_types(self) -> List[str]:
        """TODO"""
        return [f.get_type() for f in self._fields]

    def get_type(self) -> str:
        """TODO"""
        return self._type

    def get_name(self) -> str:
        """TODO"""
        return self._name

    def get_fields(self) -> List[SchemaField]:
        """TODO"""
        return self._fields

    def get_namespace(self) -> Optional[str]:
        """TODO"""
        return self._namespace

    def get_doc(self) -> Optional[str]:
        """TODO"""
        return self._doc
