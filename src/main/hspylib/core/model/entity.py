from uuid import UUID


class Entity:
    def __init__(self, table_name: str, entity_id: UUID = None):
        self._table_name = table_name.upper()
        self.uuid = entity_id

    def __str__(self):
        return "Entity( Table={} uuid={} )".format(self._table_name, str(self.uuid))

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

    def get_table_name(self) -> str:
        return self._table_name
