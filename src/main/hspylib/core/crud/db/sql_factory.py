import os
from abc import abstractmethod, ABC
from typing import Tuple

from requests.structures import CaseInsensitiveDict

from main.hspylib.core.config.app_config import AppConfigs
from main.hspylib.core.model.entity import Entity


class SqlFactory(ABC):
    @staticmethod
    def read_stubs(sql_filename: str) -> dict:
        ret_val = {}
        assert os.path.exists(sql_filename), "Sql file was not found: {}".format(sql_filename)
        with open(sql_filename) as f_stubs:
            lines = f_stubs.readlines()
            assert lines, "Stub file is empty"
            lines = list(map(str.strip, lines))
            stubs = ' '.join(lines).split(';')
            assert len(stubs) >= 4, "Stub file hasn't got the minimum stubs for [insert, select, update, delete]"
            for stub in stubs:
                if stub:
                    key = stub.strip().partition(' ')[0].lower()
                    ret_val[key] = stub.strip()
        return ret_val

    @staticmethod
    def column_set(entity: Entity) -> Tuple[str]:
        cols = []
        for key in entity.__dict__.keys():
            if not key.startswith('_'):
                cols.append(key.replace("'", "").upper())
        return tuple(cols)

    @staticmethod
    def values_set(entity: Entity) -> Tuple[str]:
        values = []
        for key, value in entity.__dict__.items():
            if not key.startswith('_'):
                values.append(str(value))
        return tuple(values)

    def __init__(self, filename: str):
        self.logger = AppConfigs.INSTANCE.logger()
        self.sql_stubs = SqlFactory.read_stubs(filename)

    @abstractmethod
    def insert(self, entity: Entity) -> str:
        pass

    @abstractmethod
    def select(self, filters: CaseInsensitiveDict) -> str:
        pass

    @abstractmethod
    def update(self, entity: Entity, filters: CaseInsensitiveDict) -> str:
        pass

    @abstractmethod
    def delete(self, filters: CaseInsensitiveDict) -> str:
        pass
