from hspylib.core.enums.enumeration import Enumeration


class Tabs(Enumeration):
    """TabWidget indexes"""
    PRODUCER = 0
    CONSUMER = 1
    REGISTRY = 2
    CONSOLE = 3


class StkTools(Enumeration):
    """StackedPane Widget 'Tools' indexes"""
    SETTINGS = 0
    SCHEMAS = 1
    STATISTICS = 2


class StkProducerEdit(Enumeration):
    """StackedPane Widget 'ProducerEdit' indexes"""
    TEXT = 0
    FORM = 1
