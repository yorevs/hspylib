from enum import Enum
from typing import List, Any


class Enumeration(Enum):

    @classmethod
    def names(cls) -> List[str]:
        return list(map(lambda e: e.name, cls))

    @classmethod
    def values(cls) -> List[Any]:
        return list(map(lambda e: e.value, cls))

    @classmethod
    def value_of(cls, name: str, ignore_case: bool = False) -> Any:
        if ignore_case:
            found = next(filter(lambda en: en.name.upper() == name.upper(), list(cls)), None)
        else:
            found = next(filter(lambda en: en.name == name, list(cls)), None)
        assert found, f"{name} is not a valid \"{cls.__name__}\" name"
        return found

    @classmethod
    def of_value(cls, value: Any, ignore_case: bool = False) -> Any:
        if ignore_case:
            found = next(filter(lambda en: str(en.value).upper() == str(value).upper(), list(cls)), None)
        else:
            found = next(filter(lambda en: en.value == value, list(cls)), None)
        assert found, f"{value} does not correspond to a valid \"{cls.__name__}\""
        return found
