from typing import Tuple
from uuid import UUID


class Entity:
    def __init__(self, entity_id: UUID = None):
        self.uuid = entity_id

    def __str__(self):
        return "Entity( uuid={} )".format(str(self.uuid))

    def to_dict(self) -> dict:
        ret_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, int):
                ret_dict[key] = int(value)
            elif isinstance(value, float):
                ret_dict[key] = float(value)
            elif isinstance(value, bool):
                ret_dict[key] = bool(value)
            else:
                ret_dict[key] = str(value)
        return ret_dict

    def to_columns(self) -> Tuple[str]:
        cols = []
        for key in self.__dict__.keys():
            if not key.startswith('_'):
                cols.append(key.replace("'", "").upper())
        return tuple(cols)

    def to_column_set(self) -> dict:
        fields = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                fields[key.replace("'", "").upper()] = "{}".format(str(value))
        return fields

    def to_values(self) -> Tuple[str]:
        values = []
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                values.append(str(value))
        return tuple(values)
