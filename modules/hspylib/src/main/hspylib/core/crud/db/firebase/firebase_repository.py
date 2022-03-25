#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.crud.db.firebase
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

from hspylib.core.crud.crud_entity import CrudEntity
from hspylib.core.crud.crud_repository import CrudRepository
from hspylib.core.crud.db.firebase.firebase_config import FirebaseConfig
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.tools.preconditions import check_not_none, check_state
from hspylib.modules.fetch.fetch import delete, get, put


class FirebaseRepository(CrudRepository):
    """TODO"""

    def __init__(self):
        self.payload = None
        self.config = FirebaseConfig()

    def __str__(self):
        return str(self.payload)

    def to_list(self, json_string: str, filters: CaseInsensitiveDict = None) -> list:
        """TODO"""
        ret_list = []
        for value in json.loads(json_string).values():
            if not filters or all(k in value and value[k] == v for k, v in filters.items()):
                ret_list.append(self.row_to_entity(value))
        return ret_list

    def insert(self, entity: CrudEntity) -> None:
        """TODO"""
        entity.uuid = entity.uuid if entity.uuid is not None else str(uuid.uuid4())
        url = f'{self.config.base_url()}/{entity.uuid}.json'
        payload = entity.to_json()
        log.debug("Inserting firebase entry: %s into: %s", entity, url)
        response = put(url, payload)
        check_not_none(response, "Response is none")
        if response.status_code != HttpCode.OK:
            raise HTTPError(f'{response.status_code} - Unable to put into={url} with json_string={payload}')

    def update(self, entity: CrudEntity) -> None:
        """TODO"""
        url = f'{self.config.base_url()}/{entity.uuid}.json'
        payload = entity.to_json()
        log.debug('Updating firebase entry: %s into: %s', entity, url)
        response = put(url, payload)
        check_not_none(response, "Response is none")
        if response.status_code != HttpCode.OK:
            raise HTTPError(f'{response.status_code} - Unable to put into={url} with json_string={payload}')

    def delete(self, entity: CrudEntity) -> None:
        """TODO"""
        url = f'{self.config.base_url()}/{entity.uuid}.json'
        log.debug('Deleting firebase entry: %s into: %s', entity, url)
        response = delete(url)
        check_not_none(response, "Response is none")
        if response.status_code != HttpCode.OK:
            raise HTTPError(f'{response.status_code} - Unable to delete from={url}')

    def find_all(self, filters: CaseInsensitiveDict = None) -> Optional[list]:
        """TODO"""
        url = f'{self.config.base_url()}.json?orderBy="$key"'
        log.debug('Fetching firebase entries from %s', url)
        response = get(url)
        check_not_none(response, "Response is none")
        if response.status_code != HttpCode.OK:
            raise HTTPError(f'{response.status_code} - Unable to get from={url}')

        return self.to_list(response.body, filters) if response.body else []

    def find_by_id(self, entity_id: str) -> Optional[CrudEntity]:
        """TODO"""
        url = f'{self.config.base_url()}.json?orderBy="$key"&equalTo="{entity_id}"'
        log.debug('Fetching firebase entry entity_id=%s from %s', entity_id, url)
        response = get(url)
        check_not_none(response, "Response is none")
        if response.status_code != HttpCode.OK:
            raise HTTPError(f'{response.status_code} - Unable to get from={url}')
        result = self.to_list(response.body) if response.body else []
        check_state(len(result) <= 1, "Multiple results found with entity_id={}", entity_id)

        return result[0] if len(result) > 0 else None

    @abstractmethod
    def row_to_entity(self, row: dict) -> CrudEntity:
        pass

    @abstractmethod
    def database_name(self) -> str:
        pass
