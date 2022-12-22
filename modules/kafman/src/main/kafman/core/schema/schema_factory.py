#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: schema_factory.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import os
from abc import ABC

from hspylib.core.preconditions import check_not_none, check_state

from kafman.core.schema.avro.avro_schema import AvroSchema
from kafman.core.schema.json.json_schema import JsonSchema
from kafman.core.schema.kafka_schema import KafkaSchema
from kafman.core.schema.plain_schema import PlainSchema


class SchemaFactory(ABC):
    """Factory method to create Avro schemas"""

    _schemas_types = [AvroSchema, JsonSchema, PlainSchema]

    @classmethod
    def create_schema(cls, filepath: str, registry_url: str) -> KafkaSchema:
        """Create a schema based on the provided file extension"""
        _, f_ext = os.path.splitext(filepath)
        schema_cls = next((schema for schema in cls._schemas_types if schema.supports(f_ext)), None)
        check_not_none(schema_cls)
        check_state(issubclass(schema_cls, KafkaSchema))

        return schema_cls(filepath, registry_url)
