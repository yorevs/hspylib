from abc import abstractmethod, ABC
from typing import Tuple

from main.hspylib.core.config.app_config import AppConfigs
from main.hspylib.core.crud.repository import Repository
from main.hspylib.core.model.entity import Entity


class DBRepository(Repository):
    def __init__(self):
        super().__init__()
        self.hostname = AppConfigs.INSTANCE.get('db.hostname')
        self.port = AppConfigs.INSTANCE.get_int('db.port')
        self.user = AppConfigs.INSTANCE.get('db.user')
        self.password = AppConfigs.INSTANCE.get('db.password')
        self.database = AppConfigs.INSTANCE.get('db.database')
        self.logger = AppConfigs.INSTANCE.logger()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def row_to_entity(self, row: Tuple) -> Entity:
        pass

    @abstractmethod
    def table_name(self) -> str:
        pass
