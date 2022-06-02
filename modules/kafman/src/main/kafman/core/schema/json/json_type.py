from collections import defaultdict
from typing import Any

from hspylib.core.enums.enumeration import Enumeration


class _JsonType(Enumeration):
    """TODO"""

    # @formatter:off
    BOOLEAN         = 'boolean'
    INTEGER         = 'integer'  # int|long
    NUMBER          = 'number'   # float|double
    STRING          = 'string'   # string|bytes|enum|fixed
    OBJECT          = 'object'   # record|map
    ARRAY           = 'array'    # array
    # @formatter:on

    def empty_value(self) -> Any:
        """TODO"""
        if self.value == 'boolean':
            return False
        elif self.value == 'integer':
            return 0
        elif self.value == 'number':
            return 0.0
        elif self.value == 'object':
            return defaultdict()
        elif self.value == 'array':
            return []
        else:
            return ''

    def is_object(self):
        return self.value == 'object'
