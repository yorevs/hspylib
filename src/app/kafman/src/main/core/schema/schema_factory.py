#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: schema_factory.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import os
from abc import ABC

from hspylib.core.tools.preconditions import check_state
from kafman.src.main.core.schema.avro_schema import AvroSchema
from kafman.src.main.core.schema.json_schema import JsonSchema
from kafman.src.main.core.schema.kafka_schema import KafkaSchema
from kafman.src.main.core.schema.plain_schema import PlainSchema


class SchemaFactory(ABC):
    """TODO"""

    _all_schemas = [
        AvroSchema,
        JsonSchema,
        PlainSchema
    ]

    @classmethod
    def create_schema(cls, filepath: str, registry_url: str) -> KafkaSchema:
        """TODO"""
        _, f_ext = os.path.splitext(filepath)
        schema_cls = next((schema for schema in cls._all_schemas if schema.supports(f_ext)), None)
        check_state(issubclass(schema_cls, KafkaSchema))

        return schema_cls(filepath, registry_url)
