import json
import uuid
from abc import abstractmethod
from typing import Optional

from requests.exceptions import HTTPError
from requests.structures import CaseInsensitiveDict

from main.hspylib.core.config.app_config import AppConfigs
from main.hspylib.core.crud.db.firebase.firebase_config import FirebaseConfig
from main.hspylib.core.crud.repository import Repository
from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.model.entity import Entity
from main.hspylib.modules.fetch.fetch import put, get


class FirebaseRepository(Repository):
    def __init__(self):
        self.logger = AppConfigs.INSTANCE.logger()
        self.payload = None
        self.config = FirebaseConfig()

    def __str__(self):
        return str(self.payload)

    def insert(self, entity: Entity):
        entity.uuid = entity.uuid if entity.uuid is not None else str(uuid.uuid4())
        url = '{}/{}.json'.format(self.config.url(), entity.uuid)
        payload = entity.to_json()
        self.logger.debug('Inserting firebase entry: {} into: {}'.format(entity, url))
        response = put(url, payload)
        assert response, "Response is empty"
        if response.status_code != HttpCode.OK:
            raise HTTPError('{} - Unable to post into={} with payload={}'.format(response.status_code, url, payload))

    def update(self, entity: Entity):
        pass

    def delete(self, entity: Entity):
        pass

    def find_all(self, filters: CaseInsensitiveDict = None) -> Optional[list]:
        url = '{}.json?orderBy="$key"'.format(self.config.url())
        self.logger.debug('Fetching firebase entries from {}'.format(url))
        response = get(url)
        assert response, "Response is empty"
        if response.status_code != HttpCode.OK:
            raise HTTPError('{} - Unable to get from={}'.format(response.status_code, url))

        return self.to_list(response.body, filters) if response.body else []

    def to_list(self, json_string: str, filters: CaseInsensitiveDict = None) -> list:
        the_list = []
        for key, value in json.loads(json_string).items():
            if all(k in value and value[k] == v for k, v in filters.items()):
                the_list.append(self.row_to_entity(value))
        return the_list

    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        pass

    @abstractmethod
    def row_to_entity(self, row: dict) -> Entity:
        pass

    @abstractmethod
    def database_name(self) -> str:
        pass
