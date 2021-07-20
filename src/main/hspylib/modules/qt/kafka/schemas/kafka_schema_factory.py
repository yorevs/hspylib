import os
from abc import ABC

from hspylib.core.tools.preconditions import check_state

from hspylib.modules.qt.kafka.schemas.kafka_plain_schema import KafkaPlainSchema

from hspylib.modules.qt.kafka.schemas.kafka_json_schema import KafkaJsonSchema

from hspylib.modules.qt.kafka.schemas.kafka_avro_schema import KafkaAvroSchema

from hspylib.modules.qt.kafka.schemas.kafka_schema import KafkaSchema


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
