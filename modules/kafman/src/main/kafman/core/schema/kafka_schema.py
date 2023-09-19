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
from typing import List, Tuple
from uuid import uuid4

from confluent_kafka.schema_registry import Schema, SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext
from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import InvalidStateError
from hspylib.core.tools.commons import build_url, file_is_not_empty, new_dynamic_object
from hspylib.core.tools.preconditions import check_not_none, check_state
from hspylib.core.tools.text_tools import strip_extra_spaces, strip_linebreaks
from hspylib.modules.qt.promotions.hstacked_widget import HStackedWidget
from jsonschema import validate as json_validate, ValidationError
from PyQt5.QtWidgets import QFrame, QLabel, QWidget

from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.schema_type import SchemaType


class KafkaSchema(ABC):
    """String schema serializer/deserializer"""

    LOCAL_REGISTRY_SERVER_URL = 'http://localhost:8081'

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

    def __init__(
        self,
        schema_type: SchemaType,
        filepath: str = None,
        registry_url: str = None,
        charset: Charset = Charset.UTF_8):

        self._schema_name = 'undefined'
        self._schema_type = schema_type.value
        self._filepath = filepath
        self._registry_url = build_url(registry_url or self.LOCAL_REGISTRY_SERVER_URL)
        self._charset = charset
        self._attributes = new_dynamic_object('SchemaAttributes')
        self._fields = None
        self._form_stack = None

        try:
            if filepath:
                check_state(file_is_not_empty(filepath), f"Schema file is empty or not found: {filepath}")
                with open(filepath, 'r', encoding=str(self._charset)) as f_schema:
                    self._content_text = strip_extra_spaces(strip_linebreaks(f_schema.read()))
                    self._content_dict = defaultdict(None, json.loads(self._content_text))
                    check_not_none(self._content_dict)
                self._parse()
                self._schema_conf = {'url': self._registry_url}
                self._schema_client = SchemaRegistryClient(self._schema_conf)
                self._schema = Schema(self._content_text, self._schema_type)
        except (KeyError, TypeError, JSONDecodeError) as err:
            err_msg = f"Unable to initialize schema ({self._registry_url}) => {str(err)}"
            log.error(err_msg)
            raise InvalidStateError(err_msg)

    def __str__(self):
        return self._schema_name

    def create_schema_form_row_widget(self, field: SchemaField) -> Tuple[QLabel, QLabel, QWidget]:
        """Create a schema form row widget"""
        pass

    def create_schema_form_widget(
        self,
        form_stack: HStackedWidget,
        parent_pane: QFrame = None,
        form_name: str = None,
        fields: List[SchemaField] = None) -> int:
        """Create the stacked frame with the form widget"""
        pass

    @abstractmethod
    def _parse(self) -> None:
        """Parse the schema content and fill in the schema attributes"""

    @abstractmethod
    def settings(self) -> dict:
        """Return the required schema settings"""

    @abstractmethod
    def form_object(self) -> dict:
        """Return the empty json schema object"""

    def get_filepath(self) -> str:
        """Return the schema file path"""
        return self._filepath

    def get_schema_type(self) -> str:
        """Return the schema type"""
        return self._schema_type

    def get_schema_name(self) -> str:
        """Return the schema name"""
        return self._schema_name

    def get_schema_fields(self) -> List['SchemaField']:
        """Return the schema fields"""
        return self._fields

    def get_content_text(self) -> str:
        """Return the schema content text"""
        return self._content_text

    def get_content_dict(self) -> dict:
        """Return the schema content dictionary"""
        return self._content_dict

    def validate(self, instance: dict) -> bool:
        """Validate current json instance. If no exception is raised by validate(), the instance is valid."""
        try:
            json_validate(instance, self._content_dict)
            return True
        except ValidationError:
            return False
