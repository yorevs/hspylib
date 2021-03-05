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
    def value_of(cls, literal: str) -> Any:
        assert literal in cls.names(), f"{literal} is not a valid \"{cls.__name__}\" name"
        return cls[literal]
