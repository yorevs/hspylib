#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: datasource
      @file: crud_entity.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from datasource.identity import Identity
from hspylib.core.namespace import Namespace
from hspylib.core.preconditions import check_argument
from typing import Any, Dict, Iterable
from uuid import UUID

import json


class CrudEntity(Namespace):
    """Generic CRUD entity type."""

    def __init__(self, entity_id: Identity | None = None, **kwargs):
        super().__init__(self.__class__.__name__, **kwargs)
        check_argument(entity_id is None or isinstance(entity_id, Identity))
        self._identity = entity_id if entity_id else Identity.auto()
        self.__iadd__(self._identity._asdict())

    @property
    def identity(self) -> Identity:
        return self._identity

    def as_dict(self) -> Dict[str, Any]:
        """Convert the entity into a dictionary object."""

        ret_dict = {}
        for key, value in zip(self.attributes, self.values):
            if isinstance(value, bool):
                ret_dict[key] = bool(value)
            elif isinstance(value, int):
                ret_dict[key] = int(value)
            elif isinstance(value, float):
                ret_dict[key] = float(value)
            elif isinstance(value, (str, UUID)):
                ret_dict[key] = str(value)
            else:
                ret_dict[key] = value.__dict__ if value else {}
        return ret_dict

    def as_json(self, indent: int = None) -> str:
        """Convert the entity into a json object."""
        return json.dumps(self.as_dict(), indent=indent)

    def as_column_set(
        self, separator: str = ", ", prefix: str | None = None, exclude: Iterable[str] | None = None
    ) -> str:
        """Return all attributes listed as tokenized 'columns = value'.
        :param separator: the separator character.
        :param prefix: an optional column prefix.
        :param exclude: a list of column names to be excluded.
        """

        column_set = []
        exclude = exclude or []
        list(
            map(
                lambda key: column_set.append(f"{key} = {(prefix or '') + key}"),
                filter(lambda a: a not in exclude, self.attributes),
            )
        )

        return separator.join(column_set)

    def as_columns(self, separator: str = ", ") -> str:
        """Return all attributes listed as tokenized 'columns'.
        :param separator: the separator character.
        """

        columns = []
        for key in self.attributes:
            columns.append(f"{key}".replace("'", ""))

        return separator.join(columns)
