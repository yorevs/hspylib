from abc import abstractmethod
from typing import Tuple

from main.hspylib.core.config.app_config import AppConfigs
from main.hspylib.core.crud.repository import Repository
from main.hspylib.core.model.entity import Entity


class DBRepository(Repository):
    def __init__(self):
        super().__init__()
        self.hostname = AppConfigs.get('db.hostname')
        self.port = AppConfigs.get_int('db.port')
        self.user = AppConfigs.get('db.user')
        self.password = AppConfigs.get('db.password')
        self.database = AppConfigs.get('db.database')
        self.logger = AppConfigs.logger()
        self.cursor = None

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
