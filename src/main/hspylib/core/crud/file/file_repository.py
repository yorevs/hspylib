import re
import uuid
from abc import abstractmethod
from typing import Optional

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.crud.file.file_storage import FileStorage
from hspylib.core.crud.repository import Repository
from hspylib.core.model.entity import Entity


class FileRepository(Repository):
    __storages = {}

    @staticmethod
    def check_criteria(partial_value, whole_value):
        if isinstance(whole_value, str):
            return str(partial_value).upper() in whole_value.upper()
        elif isinstance(whole_value, int):
            return int(partial_value) == whole_value
        elif isinstance(whole_value, float):
            return float(partial_value) == whole_value
        elif isinstance(whole_value, bool):
            return bool(partial_value) == whole_value
        else:
            return False

    def __init__(self, filename: str):
        super().__init__()
        self.logger = AppConfigs.logger()
        self.filename = filename
        self.file_db = self.__create_or_get()

    def __str__(self):
        return str(self.file_db.data)

    def __create_or_get(self):
        if self.filename in FileRepository.__storages:
            return FileRepository.__storages[self.filename]
        else:
            FileRepository.__storages[self.filename] = FileStorage(self.filename)
            return FileRepository.__storages[self.filename]

    def insert(self, entity: Entity):
        entity.uuid = entity.uuid if entity.uuid is not None else uuid.uuid4()
        self.file_db.data.append(entity.to_dict())
        self.file_db.commit()
        self.logger.debug("{} has been inserted !".format(entity.__class__.__name__))

    def update(self, entity: Entity):
        for index, next_entry in enumerate(self.file_db.data):
            if next_entry['uuid'] == entity.uuid:
                self.file_db.data[index] = entity.to_dict()
                self.file_db.commit()
                self.logger.debug("{} has been updated !".format(entity.__class__.__name__))

    def delete(self, entity: Entity):
        for index, next_entry in enumerate(self.file_db.data):
            if next_entry['uuid'] == entity.uuid:
                self.file_db.data.remove(self.file_db.data[index])
                self.file_db.commit()
                self.logger.debug("{} has been deleted !".format(entity.__class__.__name__))

    def find_all(self, filters: str = None) -> Optional[list]:
        if filters is not None:
            file_filters = filters.split(',')
            filtered = []
            for next_filter in file_filters:
                fields = re.split('=|>|<|>=|<=|==|!=', next_filter)
                try:
                    found = [
                        self.dict_to_entity(c) for c in self.file_db.data if
                        self.check_criteria(fields[1], c[fields[0]])
                    ]
                except KeyError:
                    continue
                except IndexError:
                    continue
                filtered.extend(found)
            return filtered
        else:
            return [self.dict_to_entity(c) for c in self.file_db.data]

    def find_by_id(self, entity_id: uuid.UUID) -> Optional[Entity]:
        if entity_id:
            result = [c for c in self.file_db.data if entity_id == c['uuid']]
            return result if len(result) > 0 else None
        else:
            return None

    @abstractmethod
    def dict_to_entity(self, row: dict) -> Entity:
        pass


class MyRepo(FileRepository):
    def __init__(self, filename: str):
        super().__init__(filename)

    def dict_to_entity(self, row: dict) -> Entity:
        return Entity(row[uuid])
