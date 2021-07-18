import json
from collections import defaultdict
from io import BytesIO
from typing import Any, List

import avro.schema
from avro.io import DatumReader, BinaryDecoder, DatumWriter, BinaryEncoder

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import file_is_not_empty
from hspylib.core.tools.preconditions import check_state

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

class KafkaAvroSchema:
    """Apache AVRO schema serializer/deserializer
       documentation: https://avro.apache.org/docs/current/gettingstartedpython.html
    """

    @staticmethod
    def extensions() -> List[str]:
        return ['*.avsc']

    @staticmethod
    def supports(file_extension: str) -> bool:
        """TODO"""
        return f"*{file_extension}" in KafkaAvroSchema.extensions()

    def __init__(self, filepath: str, charset: Charset = Charset.ISO8859_1):
        self._filepath = filepath
        check_state(file_is_not_empty(filepath))
        with open(filepath, 'r') as f_schema:
            schema_content = f_schema.read()
            self._content = defaultdict(None, json.loads(schema_content))
            self._type = self._content['type']
            self._namespace = self._content['namespace']
            self._name = self._content['name']
            self._fields = self._content['fields']
            self._schema = avro.schema.parse(schema_content)
            self._reader = DatumReader(self._schema)
            self._writer = DatumWriter(self._schema)
            self._charset = charset

    def __str__(self):
        return f"type={self._type},  namespace={self._namespace},  name={self._name},  fields={len(self._fields)}"

    def __repr__(self):
        return str(self)

    def decode(self, raw_bytes: bytes) -> bytes:
        """TODO"""
        bytes_writer = BytesIO(raw_bytes)
        decoder = BinaryDecoder(bytes_writer)
        datum = self._reader.read(decoder)
        return str(datum).encode(self._charset.value)

    def encode(self, msg_value: str) -> bytes:
        """TODO"""
        datum = json.loads(msg_value)
        bytes_writer = BytesIO()
        encoder = BinaryEncoder(bytes_writer)
        self._writer.write(datum, encoder)
        bytes_writer.flush()
        return bytes_writer.getvalue()

    def get_charset(self) -> str:
        return self._charset.value

    def get_field_names(self) -> List[str]:
        return [f['name'] for f in self._fields]

    def get_field_types(self) -> List[str]:
        return [f['type'] for f in self._fields]

    def get_content(self) -> str:
        return self._content

    def get_filepath(self) -> str:
        return self._filepath

    def get_type(self) -> str:
        return self._type

    def get_namespace(self) -> str:
        return self._namespace

    def get_name(self) -> str:
        return self._name

    def get_fields(self) -> List[Any]:
        return self._fields
