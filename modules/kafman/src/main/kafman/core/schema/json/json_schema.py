#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: json_schema.py
   @created: Sun, 18 Jul 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import List

from confluent_kafka.schema_registry.json_schema import JSONDeserializer, JSONSerializer
from confluent_kafka.serialization import StringDeserializer, StringSerializer
from hspylib.core.enums.charset import Charset

from kafman.core.consumer.consumer_config import ConsumerConfig
from kafman.core.producer.producer_config import ProducerConfig
from kafman.core.schema.kafka_schema import KafkaSchema
from kafman.core.schema.schema_type import SchemaType


class JsonSchema(KafkaSchema):
    """Json schema serializer/deserializer
       Documentation: https://json-schema.org/
       Additional Ref: https://docs.confluent.io/5.3.0/schema-registry/serializer-formatter.html

       E.g:.
       {
          "definitions" : {
            "record:myRecord" : {
              "type" : "object",
              "required" : [ "name", "calories" ],
              "additionalProperties" : false,
              "properties" : {
                "name" : {"type" : "string"},
                "calories" : {"type" : "number"},
                "colour" : {"type" : "string"}
              }
            }
          },
          "$ref" : "#/definitions/record:myRecord"
        }
    """

    DEFAULT_NAMESPACE = 'http://json-schema.org/draft-04/schema#'

    @classmethod
    def extensions(cls) -> List[str]:
        return ['*.json']

    def __init__(
        self,
        filepath: str,
        registry_url: str,
        charset: Charset = Charset.UTF_8):
        super().__init__(SchemaType.JSON, filepath, registry_url, charset)

    def settings(self) -> dict:
        return {
            ProducerConfig.KEY_SERIALIZER: StringSerializer(self._charset.value),
            ProducerConfig.VALUE_SERIALIZER: JSONSerializer(self._content_text, self._schema_client, self.to_dict),
            ConsumerConfig.KEY_DESERIALIZER: StringDeserializer(self._charset.value),
            ConsumerConfig.VALUE_DESERIALIZER: JSONDeserializer(self._content_text, self.from_dict)
        }

    def _parse(self) -> None:
        pass
