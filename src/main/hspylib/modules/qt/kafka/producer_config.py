from abc import ABC


class ProducerConfig(ABC):
    """TODO"""

    BOOTSTRAP_SERVERS = 'bootstrap.servers'
    KEY_SERIALIZER = 'key.serializer'
    VALUE_SERIALIZER = 'value.serializer'
    SCHEMA_REGISTRY_URL = 'schema.registry.url'
