from abc import ABC
from typing import Any

from hspylib.core.exception.exceptions import InvalidStateError


class SchemaUtils(ABC):

    @staticmethod
    def check_and_get(
        attribute: str,
        content: dict = None,
        required: bool = True,
        default: Any = None) -> Any:

        if content and attribute in content:
            return content[attribute]
        else:
            if required:
                raise InvalidStateError(f'Required attribute {attribute} was not found in content string !')

        return default