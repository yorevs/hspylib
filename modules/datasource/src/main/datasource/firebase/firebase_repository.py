#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: datasource.firebase
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
from typing import Any, Generic, List, Optional, TypeVar

from hspylib.core.enums.http_code import HttpCode
from hspylib.core.metaclass.singleton import AbstractSingleton
from hspylib.core.preconditions import check_not_none
from hspylib.modules.fetch.fetch import delete, get, put
from hspylib.modules.fetch.http_response import HttpResponse
from requests.exceptions import HTTPError

from datasource.crud_entity import CrudEntity
from datasource.firebase.firebase_configuration import FirebaseConfiguration
from datasource.identity import Identity

E = TypeVar("E", bound=CrudEntity)


class FirebaseRepository(Generic[E], metaclass=AbstractSingleton):
    """Implementation of a data access layer for a Firebase persistence store.
    API   Ref.: https://firebase.google.com/docs/reference/rest/database
    Auth  Ref.: https://firebase.google.com/docs/database/rest/auth#python
    Order Ref:. https://firebase.google.com/docs/database/rest/retrieve-data#section-rest-ordered-data
    """

    @staticmethod
    def _assert_response(response: HttpResponse, message: str) -> HttpResponse:
        check_not_none(response, "Response is none")
        if response.status_code not in [HttpCode.OK, HttpCode.ACCEPTED, HttpCode.CREATED]:
            raise HTTPError(f"{response.status_code} => {message}")
        return response

    @staticmethod
    def quote(value: Any) -> str:
        """Quote or double quote the value according to the value type."""
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
        """TODO"""
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
        """Return the database name."""
        return self._config.database

    def delete(self, entity: E) -> None:
        """Deletes the given entity from the Firebase store"""
        self.delete_by_id(entity.identity)

    def delete_by_id(self, entity_id: Identity) -> None:
        """Deletes the given entity by it's Id from the Firebase store"""
        ids = ".".join(entity_id.values)
        url = f"{self._config.url(self.table_name())}/{ids}.json"
        log.debug("Deleting firebase entry: \n\t|-Id=%s\n\t|-From %s", entity_id, url)
        self._assert_response(delete(url), f"Unable to delete from={url}")

    def delete_all(self, entities: List[E]) -> None:
        """Delete from Firebase all entries provided.
        TODO Check if there is a better ways of doing it.
        """
        list(map(self.delete, entities))

    def save(self, entity: E) -> None:
        """Saves the given entity at the Firebase store"""
        ids = ".".join(entity.identity.values)
        url = f"{self._config.url(self.table_name())}/{ids}.json"
        payload = entity.as_json()
        log.debug("Saving firebase entry: \n\t|-%s \n\t|-Into %s", entity, url)
        self._assert_response(put(url, payload), f"Unable to put into={url} with json_string={payload}")

    def save_all(self, entities: List[E]) -> None:
        """Save from Firebase all entries provided.
        TODO Check if there is a better ways of doing it.
        """
        list(map(self.save, entities))

    def find_all(
        self,
        order_by: Optional[List[str]] = None,
        limit_to_first: Optional[int] = None,
        limit_to_last: Optional[int] = None,
        start_at: Optional[int | str] = None,
        end_at: Optional[int | str] = None,
        equal_to: Optional[int | str] = None,
    ) -> List[E]:
        """Return filtered entries from the Firebase store"""

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
        """Return the entry specified by ID from the Firebase store, None if no such entry is found."""
        ids = ".".join(entity_id.values)
        url = f"{self._config.url(self.table_name())}/{ids}.json"
        log.debug("Fetching firebase entry: \n\t|-Id=%s\n\t|-From %s", entity_id, url)
        response = self._assert_response(get(url), f"Unable to get from={url}")
        if response.body and response.body != "null":
            return self.to_entity_type(json.loads(response.body))

        return None

    def exists_by_id(self, entity_id: Identity) -> bool:
        """Check if provided entity exists on the database.
        TODO Check if there is a better ways of doing it.
        """
        return self.find_by_id(entity_id) is not None

    @abstractmethod
    def to_entity_type(self, entity_dict: dict | tuple) -> E:
        """TODO"""

    @abstractmethod
    def table_name(self) -> str:
        """TODO"""

    def to_entity_list(self, json_string: str) -> List[E]:
        """Return filtered entries from the json_string as a list"""
        if json_string and (entities := json.loads(json_string)):
            ret_list = []
            list(map(lambda v: ret_list.append(self.to_entity_type(v)), entities.values()))
            return ret_list
        return []
