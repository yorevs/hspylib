#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.crud.db.firebase
      @file: firebase_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import json
import logging as log
import uuid
from abc import abstractmethod
from typing import Optional

from requests.exceptions import HTTPError
from requests.structures import CaseInsensitiveDict

from hspylib.core.crud.crud_repository import CrudRepository
from hspylib.core.crud.db.firebase.firebase_config import FirebaseConfig
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.model.entity import Entity
from hspylib.modules.fetch.fetch import delete, get, put


class FirebaseRepository(CrudRepository):
    def __init__(self):
        self.payload = None
        self.config = FirebaseConfig()
    
    def __str__(self):
        return str(self.payload)
    
    def to_list(self, json_string: str, filters: CaseInsensitiveDict = None) -> list:
        the_list = []
        for value in json.loads(json_string).values():
            if not filters or all(k in value and value[k] == v for k, v in filters.items()):
                the_list.append(self.row_to_entity(value))
        return the_list
    
    def insert(self, entity: Entity) -> None:
        entity.uuid = entity.uuid if entity.uuid is not None else str(uuid.uuid4())
        url = '{}/{}.json'.format(self.config.base_url(), entity.uuid)
        payload = entity.to_json()
        log.debug('Inserting firebase entry: {} into: {}'.format(entity, url))
        response = put(url, payload)
        assert response, "Response is empty"
        if response.status_code != HttpCode.OK:
            raise HTTPError('{} - Unable to put into={} with json_string={}'.format(response.status_code, url, payload))
    
    def update(self, entity: Entity) -> None:
        url = '{}/{}.json'.format(self.config.base_url(), entity.uuid)
        payload = entity.to_json()
        log.debug('Updating firebase entry: {} into: {}'.format(entity, url))
        response = put(url, payload)
        assert response, "Response is empty"
        if response.status_code != HttpCode.OK:
            raise HTTPError('{} - Unable to put into={} with json_string={}'.format(response.status_code, url, payload))
    
    def delete(self, entity: Entity) -> None:
        url = '{}/{}.json'.format(self.config.base_url(), entity.uuid)
        log.debug('Deleting firebase entry: {} into: {}'.format(entity, url))
        response = delete(url)
        assert response, "Response is empty"
        if response.status_code != HttpCode.OK:
            raise HTTPError('{} - Unable to delete from={}'.format(response.status_code, url))
    
    def find_all(self, filters: CaseInsensitiveDict = None) -> Optional[list]:
        url = '{}.json?orderBy="$key"'.format(self.config.base_url())
        log.debug('Fetching firebase entries from {}'.format(url))
        response = get(url)
        assert response, "Response is empty"
        if response.status_code != HttpCode.OK:
            raise HTTPError('{} - Unable to get from={}'.format(response.status_code, url))
        
        return self.to_list(response.body, filters) if response.body else []
    
    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        url = '{}.json?orderBy="$key"&equalTo="{}"'.format(self.config.base_url(), entity_id)
        log.debug('Fetching firebase entry entity_id={} from {}'.format(entity_id, url))
        response = get(url)
        assert response, "Response is empty"
        if response.status_code != HttpCode.OK:
            raise HTTPError('{} - Unable to get from={}'.format(response.status_code, url))
        result = self.to_list(response.body) if response.body else []
        assert len(result) <= 1, "Multiple results found with entity_id={}".format(entity_id)
        
        return result[0] if len(result) > 0 else None
    
    @abstractmethod
    def row_to_entity(self, row: dict) -> Entity:
        pass
    
    @abstractmethod
    def database_name(self) -> str:
        pass
