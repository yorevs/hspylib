#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: datasource
      @file: crud_entity.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import json
from typing import Iterable
from uuid import UUID

from hspylib.core.namespace import Namespace
from hspylib.core.preconditions import check_argument

from datasource.identity import Identity


class CrudEntity(Namespace):
    """Generic entity type."""

    def __init__(self, entity_id: Identity | None = None, **kwargs):
        super().__init__(self.__class__.__name__, **kwargs)
        check_argument(entity_id is None or isinstance(entity_id, Identity))
        self._identity = entity_id if entity_id else Identity.auto()
        self.__iadd__(self._identity._asdict())

    @property
    def identity(self) -> Identity:
        return self._identity

    def as_dict(self) -> dict:
        """TODO"""

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
        """TODO"""
        return json.dumps(self.as_dict(), indent=indent)

    def as_column_set(
        self,
        separator: str = ", ",
        prefix: str | None = None,
        exclude: Iterable[str] | None = None
    ) -> str:
        """TODO"""

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
        """TODO"""

        columns = []
        for key in self.attributes:
            columns.append(f"{key}".replace("'", ""))

        return separator.join(columns)
