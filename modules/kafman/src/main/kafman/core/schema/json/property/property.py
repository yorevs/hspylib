from typing import Any

from kafman.core.schema.json.json_type import JsonType


class Property:
    """TODO"""

    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        p_type: JsonType,
        default: Any = None,
        required: bool = True):

        self.name = name
        self.title = title
        self.description = description
        self.type = p_type
        self.default = default
        self.required = required
        self.all_properties = None
        self.all_symbols = None
