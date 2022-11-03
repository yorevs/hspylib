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

   Copyright 2022, HSPyLib team
"""

import json
import logging as log
from abc import abstractmethod
from typing import Iterable, List, Optional, Set, TypeVar

from requests.exceptions import HTTPError

from hspylib.core.datasource.crud_entity import CrudEntity
from hspylib.core.datasource.crud_repository import CrudRepository
from hspylib.core.datasource.firebase.firebase_configuration import FirebaseConfiguration
from hspylib.core.datasource.identity import Identity
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.namespace import Namespace
from hspylib.modules.fetch.fetch import delete, get, put

T = TypeVar('T', bound=CrudEntity)


class FirebaseRepository(CrudRepository[T]):
    """Implementation of a data access layer for a Firebase persistence store."""

    def __init__(self, config: FirebaseConfiguration):
        self._payload = None
        self._config = config

    def __str__(self) -> str:
        return str(self._config) + f"TABLE_NAME={self.table_name() or ''}"

    def __repr__(self):
        return str(self)

    @property
    def config(self) -> FirebaseConfiguration:
        return self._config

    @property
    def info(self) -> str:
        return f"{self.config}"

    @property
    def hostname(self) -> str:
        return self._config.hostname

    @property
    def port(self) -> int:
        return self._config.port

    @property
    def base_url(self) -> str:
        return self._config.base_url

    @property
    def database(self) -> str:
        """Return the database name."""
        return self._config.database

    def delete(self, entity: T) -> None:
        """Deletes the given entity from the Firebase store"""
        self.delete_by_id(entity.identity)

    def delete_by_id(self, entity_id: Identity) -> None:
        """Deletes the given entity by it's Id from the Firebase store"""
        ids = '.'.join(entity_id.values)
        url = f'{self._config.url(self.table_name())}/{ids}.json'
        log.debug('Deleting firebase entry: \n\t|-Id=%s\n\t|-From %s', entity_id, url)
        response = delete(url)
        check_not_none(response, "Response is none")
        if response.status_code != HttpCode.OK:
            raise HTTPError(f'{response.status_code} - Unable to delete from={url}')

    def delete_all(self, entities: List[T]) -> None:
        """Delete from Firebase all entries provided.
        TODO Check if there is a better ways of doing it.
        """
        list(map(self.delete, entities))

    def save(self, entity: T, exclude_update: Iterable[str] = None) -> None:
        """Saves the given entity at the Firebase store"""
        ids = '.'.join(entity.identity.values)
        url = f'{self._config.url(self.table_name())}/{ids}.json'
        payload = entity.as_json()
        log.debug("Saving firebase entry: \n\t|-%s \n\t|-Into %s", entity, url)
        response = put(url, payload)
        check_not_none(response, "Response is none")
        if response.status_code not in [HttpCode.OK, HttpCode.ACCEPTED]:
            raise HTTPError(f'{response.status_code} - Unable to put into={url} with json_string={payload}')

    def save_all(self, entities: List[T], exclude_update: Iterable[str] = None) -> None:
        """Save from Firebase all entries provided.
        TODO Check if there is a better ways of doing it.
        """
        list(map(self.save, entities))

    def find_all(
        self,
        fields: Set[str] = None,
        filters: Namespace = None,
        limit: int = 500, offset: int = 0) -> List[T]:
        """Return filtered entries from the Firebase store"""

        url = f'{self._config.url(self.table_name())}.json?orderBy="$key"'
        log.debug('Fetching firebase entries: \n\t|-From %s', url)
        response = get(url)
        check_not_none(response, "Response is none")
        if response.status_code != HttpCode.OK:
            raise HTTPError(f'{response.status_code} - Unable to get from={url}')

        if response.body and response.body != 'null':
            return self.to_entity_list(response.body, filters)

        return []

    def find_by_id(self, entity_id: Identity, fields: Set[str] = None) -> Optional[T]:
        """Return the entry specified by ID from the Firebase store, None if no such entry is found."""
        ids = '.'.join(entity_id.values)
        url = f'{self._config.url(self.table_name())}/{ids}.json'
        log.debug('Fetching firebase entry: \n\t|-Id=%s\n\t|-From %s', entity_id, url)
        response = get(url)
        check_not_none(response, "Response is null")
        if response.status_code != HttpCode.OK:
            raise HTTPError(f'{response.status_code} - Unable to get from={url}')
        if response.body and response.body != 'null':
            return self.to_entity_type(json.loads(response.body))

        return None

    def exists_by_id(self, entity_id: Identity) -> bool:
        """Check if provided entity exists on the database.
        TODO Check if there is a better ways of doing it.
        """
        return self.find_by_id(entity_id) is not None

    @abstractmethod
    def table_name(self) -> str:
        """TODO"""
