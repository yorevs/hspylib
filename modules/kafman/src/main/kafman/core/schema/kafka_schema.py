#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: kafka_schema.py
   @created: Sum, 18 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from abc import ABC, abstractmethod
from avro.schema import SchemaParseException
from collections import defaultdict
from confluent_kafka.schema_registry import Schema, SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext
from hspylib.core.enums.charset import Charset
from hspylib.core.namespace import Namespace
from hspylib.core.preconditions import check_not_none, check_state
from hspylib.core.tools.commons import file_is_not_empty
from hspylib.core.tools.text_tools import strip_extra_spaces, strip_linebreaks
from hspylib.modules.fetch.uri_builder import UriBuilder
from hspylib.modules.qt.promotions.hstacked_widget import HStackedWidget
from json.decoder import JSONDecodeError
from kafman.core.exception.exceptions import InvalidSchemaError
from kafman.core.schema.schema_field import SchemaField
from kafman.core.schema.schema_type import SchemaType
from kafman.core.schema.widget_utils import INPUT_WIDGET
from kafman.views.promotions.form_pane import FormPane
from PyQt5.QtWidgets import QLabel
from typing import List, Tuple
from uuid import uuid4

import json
import logging as log


class KafkaSchema(ABC):
    """Generic Kafka avro schema"""

    LOCAL_REGISTRY_SERVER_URL = "http://localhost:8081"

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

    @staticmethod
    def create_schema_form_row_widget(field: SchemaField) -> Tuple[QLabel, QLabel, INPUT_WIDGET]:
        """Create a schema form row widget"""

        check_not_none(field)
        field_name = field.name.replace("_", " ").title()
        label = QLabel(f"{field_name}: ")
        if field.required:
            req_label = QLabel("*")
            req_label.setStyleSheet("QLabel {color: #FF554D;}")
        else:
            req_label = QLabel(" ")
        req_label.setToolTip(f"This field is {'required' if field.required else 'optional'}")
        input_widget = field.create_input_widget()

        return req_label, label, input_widget

    def __init__(
        self, schema_type: SchemaType, filepath: str = None, registry_url: str = None, charset: Charset = Charset.UTF_8
    ):

        self._schema_name = "undefined"
        self._schema_type = schema_type
        self._filepath = filepath
        self._registry_url = UriBuilder.ensure_scheme(registry_url or self.LOCAL_REGISTRY_SERVER_URL)
        self._charset = charset
        self._attributes = Namespace("SchemaAttributes")
        self._json_template = defaultdict()
        self._form_stack = None

        try:
            if filepath:
                check_state(file_is_not_empty(filepath), f"Schema file is empty or not found: {filepath}")
                with open(filepath, "r", encoding=str(self._charset)) as f_schema:
                    self._content_text = strip_extra_spaces(strip_linebreaks(f_schema.read()))
                    self._content_dict = defaultdict(None, json.loads(self._content_text))
                    check_not_none(self._content_dict)
                self._parse()
                self._schema_conf = {"url": self._registry_url}
                self._schema_client = SchemaRegistryClient(self._schema_conf)
                self._schema = Schema(self._content_text, self._schema_type.name)
        except (KeyError, TypeError, JSONDecodeError, SchemaParseException) as err:
            err_msg = f"Unable to initialize schema ({self._registry_url}) => {str(err)}"
            log.error(err_msg)
            raise InvalidSchemaError(err_msg) from err

    def __str__(self):
        return self._attributes.name

    def create_schema_form_widget(
        self,
        form_stack: HStackedWidget,
        parent_pane: FormPane = None,
        form_name: str = None,
        fields: List[SchemaField] = None,
    ) -> int:
        """Create the stacked frame with the form widget"""

    @abstractmethod
    def _parse(self) -> None:
        """Parse the schema content and fill in the schema attributes"""

    @abstractmethod
    def settings(self) -> dict:
        """Return the required schema settings"""

    def validate(self, json_form: dict) -> None:
        """Validate the json form against the schema"""

    def get_filepath(self) -> str:
        """Return the schema file path"""
        return self._filepath

    def get_schema_type(self) -> str:
        """Return the schema type"""
        return self._schema_type.name

    def get_schema_name(self) -> str:
        """Return the schema name"""
        return self._schema_name

    def get_schema_fields(self) -> List["SchemaField"]:
        """Return the schema fields"""
        return self._attributes.fields

    def get_content_text(self) -> str:
        """Return the schema content text"""
        return self._content_text

    def get_content_dict(self) -> dict:
        """Return the schema content dictionary"""
        return self._content_dict
