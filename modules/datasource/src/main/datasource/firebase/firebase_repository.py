#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: datasource.firebase
      @file: firebase_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from abc import abstractmethod
from datasource.crud_entity import CrudEntity
from datasource.firebase.firebase_configuration import FirebaseConfiguration
from datasource.identity import Identity
from hspylib.core.metaclass.singleton import AbstractSingleton
from hspylib.core.namespace import Namespace
from hspylib.core.preconditions import check_not_none
from hspylib.modules.fetch.fetch import delete, get, put
from hspylib.modules.fetch.http_response import HttpResponse
from requests.exceptions import HTTPError
from typing import Any, Generic, List, Optional, TypeVar

import json
import logging as log

E = TypeVar("E", bound=CrudEntity)


class FirebaseRepository(Generic[E], metaclass=AbstractSingleton):
    """Implementation of a data access layer for a Firebase persistence store.
    API   Ref.: https://firebase.google.com/docs/reference/rest/database
    Auth  Ref.: https://firebase.google.com/docs/database/rest/auth#python
    Order Ref:. https://firebase.google.com/docs/database/rest/retrieve-data#section-rest-ordered-data
    """

    @staticmethod
    def _assert_response(response: HttpResponse, message: str) -> HttpResponse:
        """Assert that the specified response code is from 2xx.
        :param response: the http response object.
        :param message: the error message to be raised if the response code is from 2xx.
        """
        check_not_none(response, "Response is none")
        if not response.status_code.is_2xx():
            raise HTTPError(f"{response.status_code} => {message}")
        return response

    @staticmethod
    def quote(value: Any) -> str:
        """Quote or double quote the value according to the value type.
        :param value: the value to be quoted.
        """
        if isinstance(value, bool):
            return f"{str(value).lower()}"
        if isinstance(value, int | float):
            return str(value)

        return f'"{value}"' if value.startswith("'") and value.endswith("'") else f"'{value}'"

    def __init__(self, config: FirebaseConfiguration):
        self._payload = None
        self._config = config

    def __str__(self) -> str:
        return str(self._config) + f"TABLE_NAME={self.table_name() or ''}"

    def __repr__(self) -> str:
        return str(self)

    @property
    def logname(self) -> str:
        return self.__class__.__name__.split("_", maxsplit=1)[0]

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
        return self._config.database

    def delete(self, entity: E) -> None:
        """Deletes a given entity.
        :param entity: the entity to delete.
        """
        self.delete_by_id(entity.identity)

    def delete_by_id(self, entity_id: Identity) -> None:
        """Deletes the entity with the given id.
        :param entity_id: the ID of the entity to be deleted.
        """
        ids = ".".join(entity_id.values)
        url = f"{self._config.url(self.table_name())}/{ids}.json"
        log.debug("Deleting firebase entry: \n\t|-Id=%s\n\t|-From %s", entity_id, url)
        self._assert_response(delete(url), f"Unable to delete from={url}")

    def delete_all(self, entities: List[E]) -> None:
        """Deletes all given entities.
        TODO Check if there is a better way of doing it.
        :param entities: the entities to be deleted.
        """
        list(map(self.delete, entities))

    def save(self, entity: E) -> None:
        """Saves a given entity.
        :param entity: the entity to save.
        """
        ids = ".".join(entity.identity.values)
        url = f"{self._config.url(self.table_name())}/{ids}.json"
        payload = entity.as_json()
        log.debug("Saving firebase entry: \n\t|-%s \n\t|-Into %s", entity, url)
        self._assert_response(put(url, payload), f"Unable to put into={url} with json_string={payload}")

    def save_all(self, entities: List[E]) -> None:
        """Saves all given entities.
        TODO Check if there is a better way of doing it.
        :param entities: the entities to be saved.
        """
        list(map(self.save, entities))

    def find_all(
        self,
        order_by: List[str] | None = None,
        limit_to_first: int | None = None,
        limit_to_last: int | None = None,
        start_at: int | str | None = None,
        end_at: int | str | None = None,
        equal_to: int | str | None = None,
    ) -> List[E]:
        """Returns all entities of the type.
        :param order_by: result set order by.
        :param limit_to_first: the maximum number of entries to be fetch (first N entries).
        :param limit_to_last: the maximum number of entries to be fetch (last N entries).
        :param start_at: arbitrary starting points for queries.
        :param end_at: arbitrary ending points for your queries.
        :param equal_to: the maximum number of entries to be fetch.
        """

        f_order_by = "orderBy=" + (",".join([f'"{o}"' for o in order_by]) if order_by else '"$key"')
        f_start_at = f"&startAt={self.quote(start_at)}" if start_at else ""
        f_end_at = f"&endAt={self.quote(end_at)}" if end_at else ""
        f_equal_to = f"&equalTo={self.quote(equal_to)}" if equal_to else ""
        f_limit_first = f"&limitToFirst={limit_to_first}" if limit_to_first else ""
        f_limit_last = f"&limitToLast={limit_to_last}" if limit_to_last else ""
        url = (
            f"{self._config.url(self.table_name())}.json?"
            f"{f_order_by}{f_start_at}{f_end_at}{f_equal_to}{f_limit_first}{f_limit_last}"
        )
        log.debug("Fetching firebase entries: \n\t|-From %s", url)
        response = self._assert_response(get(url), f"Unable to get from={url}")
        if response.body and response.body != "null":
            return self.to_entity_list(response.body)

        return []

    def find_by_id(self, entity_id: Identity) -> Optional[E]:
        """Return the entity specified by ID from the Firebase store, None if no such entry is found."""
        ids = ".".join(entity_id.values)
        url = f"{self._config.url(self.table_name())}/{ids}.json"
        log.debug("Fetching firebase entry: \n\t|-Id=%s\n\t|-From %s", entity_id, url)
        response = self._assert_response(get(url), f"Unable to get from={url}")
        if response.body and response.body != "null":
            return self.to_entity_type(json.loads(response.body))

        return None

    def exists_by_id(self, entity_id: Identity) -> bool:
        """Returns whether an entity with the given id exists.
        TODO Check if there is a better way of doing it.
        :param entity_id: the entity ID.
        """
        return self.find_by_id(entity_id) is not None

    @abstractmethod
    def to_entity_type(self, entity_dict: dict | tuple) -> E:
        """Convert a dict or tuple, generally from a result set, into the CRUD entity.
        :param entity_dict: the entity dict or tuple to be converted.
        """

    @abstractmethod
    def table_name(self) -> str:
        """Return the table name (repository name)."""

    def to_entity_list(self, json_string: str, filters: Namespace | None = None) -> List[E]:
        """Return filtered entries from the json_string as a list.
        :param json_string: the json string to be parsed.
        :param filters: entry filters.
        """
        ret_list = []
        for value in json.loads(json_string).values():
            if not filters or all(k in value and value[k] == v for k, v in filters.items()):
                ret_list.append(self.to_entity_type(value))
        return ret_list
