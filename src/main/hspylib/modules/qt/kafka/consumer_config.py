from abc import ABC


class ConsumerConfig(ABC):
    """TODO"""

    BOOTSTRAP_SERVERS = 'bootstrap.servers'
    GROUP_ID = 'group.id'
    CLIENT_ID = 'client.id'
    ENABLE_AUTO_COMMIT = 'enable.auto.commit'
    SESSION_TIMEOUT_MS = 'session.timeout.ms'
    AUTO_OFFSET_RESET = 'auto.offset.reset'
    KEY_DESERIALIZER = 'key.deserializer'
    VALUE_DESERIALIZER = 'value.deserializer'
