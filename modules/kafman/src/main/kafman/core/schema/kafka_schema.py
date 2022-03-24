#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
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
from typing import Any, List, Optional
from uuid import uuid4

from confluent_kafka.schema_registry import Schema, SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext
from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import InvalidStateError
from hspylib.core.tools.commons import build_url, file_is_not_empty, syserr
from hspylib.core.tools.preconditions import check_not_none, check_state
from hspylib.core.tools.text_tools import remove_linebreaks


class KafkaSchema(ABC):
    """String schema serializer/deserializer"""

    @classmethod
    def extensions(cls) -> List[str]:
        """Return the supported schema file extensions"""
        return []

    @classmethod
    def supports(cls, file_extension: str) -> bool:
        """Check if the provided file extension is supported by the schema"""
        return f"*{file_extension}" in cls.extensions()

    @classmethod
    def to_dict(cls, obj: str, ctx: SerializationContext) -> dict:  # pylint: disable=unused-argument
        """Return a function to convert the string object into the schema dict"""
        return json.loads(obj)

    @classmethod
    def from_dict(cls, obj: dict, ctx: SerializationContext) -> str:  # pylint: disable=unused-argument
        return json.dumps(obj)

    @classmethod
    def key(cls) -> str:
        """Generate a new schema key for registration"""
        return str(uuid4())

    @classmethod
    def get_items(cls, field_attrs: dict) -> List[str]:  # pylint: disable=unused-argument
        return []

    def __init__(
        self,
        schema_type: str,
        filepath: str = None,
        registry_url: str = None,
        charset: Charset = Charset.ISO8859_1):

        self._filepath = filepath
        self._registry_url = registry_url
        self._avro_type = schema_type
        self._charset = charset
        self._fields = None
        self._schema_id = None
        self._namespace = None
        self._doc = None
        self._name = None
        self._type = None

        try:
            if filepath:
                check_state(file_is_not_empty(filepath), f"Schema file not found: {filepath}")
                with open(filepath, 'r', encoding='utf-8') as f_schema:
                    self._schema_str = remove_linebreaks(f_schema.read())
                    self._content = defaultdict(None, json.loads(self._schema_str))
                    check_not_none(self._content)
                self._schema_conf = {'url': build_url(self._registry_url) or 'http://localhost:8081'}
                self._schema_client = SchemaRegistryClient(self._schema_conf)
                self._schema = Schema(self._schema_str, self._avro_type)
                self._parse()
        except (KeyError, TypeError, JSONDecodeError) as err:
            err_msg = f"Unable to initialize schema => {str(err)}"
            syserr(err_msg)
            log.error(err_msg)
            raise InvalidStateError(err_msg)

    def __getitem__(self, index: int):
        return self._fields[index]

    def __str__(self):
        return f"[{self._avro_type}] name={self._name}, type={self._type}, namespace={self._namespace}"

    def __repr__(self):
        return self._avro_type

    @abstractmethod
    def _parse(self) -> None:
        """Parse the schema content and fill in the schema attributes"""

    @abstractmethod
    def serializer_settings(self) -> dict:
        """Return the required serializer settings for the schema"""

    @abstractmethod
    def deserializer_settings(self) -> dict:
        """Return the required deserializer settings for the schema"""

    def get_avro_type(self) -> str:
        """Return the schema type"""
        return self._avro_type

    def get_filepath(self) -> str:
        """Return the schema file path"""
        return self._filepath

    def get_charset(self) -> str:
        """Return the schema charset"""
        return self._charset.value

    def get_content(self) -> dict:
        """Return the schema content"""
        return self._content

    def get_type(self) -> str:
        """Return the schema type"""
        return self._type

    def get_name(self) -> str:
        """Return the schema name"""
        return self._name

    def get_namespace(self) -> Optional[str]:
        """Return the schema namespace"""
        return self._namespace

    def get_doc(self) -> Optional[str]:
        """Return the schema description"""
        return self._doc

    def get_fields(self, sort_by_required: bool = True) -> List[Any]:
        """Return the schema fields"""
        return [] if not self._fields else self._fields \
            if not sort_by_required \
            else sorted(self._fields, key=lambda f: f.is_required(), reverse=True)
