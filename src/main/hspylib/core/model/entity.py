import json
from typing import Tuple
from uuid import UUID


class Entity:
    def __init__(self, entity_id: UUID = None):
        self.uuid = entity_id

    def __str__(self):
        return "Entity( uuid={} )".format(str(self.uuid))

    def __eq__(self, other):
        return isinstance(other, Entity) and all(item in self.to_dict().items() for item in other.to_dict().items())

    def to_dict(self) -> dict:
        ret_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, bool):
                ret_dict[key] = bool(value)
            elif isinstance(value, int):
                ret_dict[key] = int(value)
            elif isinstance(value, float):
                ret_dict[key] = float(value)
            elif isinstance(value, str):
                ret_dict[key] = str(value)
            else:
                ret_dict[key] = None
        return ret_dict

    def to_json(self):
        dict_obj = self.to_dict()
        json_str = json.dumps(dict_obj)
        return json_str

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
