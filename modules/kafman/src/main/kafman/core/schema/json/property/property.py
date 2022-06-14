from typing import Any, List, Union

from hspylib.core.exception.exceptions import InvalidArgumentError
from hspylib.core.tools.commons import new_dynamic_object
from hspylib.core.tools.preconditions import check_and_get

from kafman.core.schema.json.json_type import JsonType


class Property:
    """TODO"""

    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        s_type: JsonType,
        default: Any = None,
        required: bool = True):

        self.name = name
        self.title = title
        self.description = description
        self.type = s_type
        self.default = default
        self.required = required
        self.all_properties = None
        self.extras = new_dynamic_object('SchemaAttributes')

    def set_items(self, p_items: Union[List[str], dict]) -> None:
        """TODO"""
        if isinstance(p_items, list):
            self.extras.a_items = p_items
        elif isinstance(p_items, dict):
            self.extras.enum = check_and_get('enum', p_items, False, [])
        else:
            raise InvalidArgumentError(f'Invalid property \"items\" type: {type(p_items)}')
        pass
