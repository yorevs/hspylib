#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: kafka_schema_factory.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import os
from abc import ABC

from hspylib.core.tools.preconditions import check_state
from kafman.src.main.core.kafka.schemas.kafka_avro_schema import KafkaAvroSchema
from kafman.src.main.core.kafka.schemas.kafka_json_schema import KafkaJsonSchema
from kafman.src.main.core.kafka.schemas.kafka_plain_schema import KafkaPlainSchema
from kafman.src.main.core.kafka.schemas.kafka_schema import KafkaSchema


class KafkaSchemaFactory(ABC):
    _all_schemas = [
        KafkaAvroSchema,
        KafkaJsonSchema,
        KafkaPlainSchema
    ]

    @classmethod
    def create_schema(cls, filepath: str, registry_url: str) -> KafkaSchema:
        _, f_ext = os.path.splitext(filepath)
        schema_cls = next((schema for schema in cls._all_schemas if schema.supports(f_ext)), None)
        check_state(issubclass(schema_cls, KafkaSchema))

        return schema_cls(filepath, registry_url)
