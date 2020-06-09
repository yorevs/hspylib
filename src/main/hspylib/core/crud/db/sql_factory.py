import os
from abc import abstractmethod, ABC
from typing import List, Optional

from main.hspylib.core.config.app_config import AppConfigs
from main.hspylib.core.model.entity import Entity
from requests.structures import CaseInsensitiveDict


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
    def join_filters(filters: CaseInsensitiveDict, join_operator: str = 'AND') -> str:
        filter_string = ''
        if filters:
            for key, value in filters.items():
                filter_string += "{} {} = '{}'".format(join_operator, key, value)
        return filter_string

    @staticmethod
    def join_fieldset(entity: Entity) -> str:
        fields = entity.to_column_set()
        field_set = ''
        for key, value in fields.items():
            field_set += "{}{} = '{}'".format(', ' if field_set else '', key, value)
        return field_set

    def __init__(self, filename: str):
        self.logger = AppConfigs.INSTANCE.logger()
        self.sql_stubs = SqlFactory.read_stubs(filename)

    @abstractmethod
    def insert(self, entity: Entity) -> Optional[str]:
        pass

    @abstractmethod
    def select(self, column_set: List[str], filters: CaseInsensitiveDict) -> Optional[str]:
        pass

    @abstractmethod
    def update(self, entity: Entity, filters: CaseInsensitiveDict) -> Optional[str]:
        pass

    @abstractmethod
    def delete(self, filters: CaseInsensitiveDict) -> Optional[str]:
        pass
