#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: datasource
      @file: identity.py
   @created: Thu, 03 Nov 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from collections import namedtuple
from hspylib.core.namespace import Namespace
from hspylib.core.preconditions import check_argument
from typing import Any, Dict, Tuple, Type, Union
from uuid import UUID, uuid4

import random
import string
import sys

IDENTITY = Union[Tuple, int, str, UUID]


class Identity(Namespace):
    """Represent a unique identity of an entity."""

    @classmethod
    def auto(cls, field_name: str = "id", id_type: Type = UUID) -> "Identity":
        """Automatically assigns a value for the identity.
        :param field_name: the identity field name.
        :param id_type: the type of the identity.
        """
        _id_ = namedtuple("Identity", [f"{field_name}"])
        match id_type.__name__:
            case "int":
                number = random.randint(0, sys.maxsize)
                return Identity(_id_(number))
            case "str":
                letters = string.ascii_lowercase + "-_"
                st = "".join(random.choice(letters) for _ in range(32))
                return Identity(_id_(st))
            case "UUID":
                return Identity(_id_(uuid4().hex))
            case other:
                raise NotImplementedError(f"auto-identity generator for type '{other}' is not implemented")

    def __init__(self, identity: Tuple | Namespace | "Identity"):
        check_argument(isinstance(identity, Tuple | Identity | Namespace), "Must be a named tuple or Identity")
        identity = identity.ID if isinstance(identity, Identity) else identity
        self._identity = identity
        super().__init__("Identity", **self._asdict())

    def __str__(self) -> str:
        return str(self._identity)

    @property
    def ID(self) -> Tuple:
        return self._identity

    def _asdict(self) -> Dict[str, Any]:
        """Return a new dict which maps field names to their values."""
        return self._identity._asdict()

    def as_column_set(self, separator: str = ",") -> str:
        """Return all attributes listed as tokenized 'columns = value'.
        :param separator: the separator character.
        """
        column_set = []
        list(map(lambda key, value: column_set.append(f"{key} = {value}"), self.attributes, self.values))
        return separator.join(column_set)
