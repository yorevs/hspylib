#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: kafka_schema.py
   @created: Sum, 18 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Any
from uuid import uuid4

from hspylib.core.enums.charset import Charset


class KafkaSchema(ABC):
    """String schema serializer/deserializer"""

    @classmethod
    def extensions(cls) -> List[str]:
        """TODO"""
        pass

    @classmethod
    def supports(cls, file_extension: str) -> bool:
        """TODO"""
        return f"*{file_extension}" in cls.extensions()

    @classmethod
    def to_dict(cls, obj: Any, ctx) -> dict:
        """TODO"""
        pass

    @classmethod
    def from_dict(cls, obj: dict, ctx) -> Any:
        """TODO"""
        pass

    @classmethod
    def key(cls) -> str:
        """TODO"""
        return str(uuid4())

    def __init__(self, filepath: str = None, charset: Charset = Charset.ISO8859_1):
        self._filepath = filepath
        self._charset = charset

    @abstractmethod
    def serializer_settings(self) -> dict:
        """TODO"""
        pass

    @abstractmethod
    def deserializer_settings(self) -> dict:
        """TODO"""
        pass

    @abstractmethod
    def get_field_names(self) -> List[str]:
        """TODO"""
        pass

    @abstractmethod
    def get_field_types(self) -> List[str]:
        """TODO"""
        pass

    @abstractmethod
    def get_content(self) -> defaultdict:
        """TODO"""
        pass

    @abstractmethod
    def get_type(self) -> str:
        """TODO"""
        pass

    def get_filepath(self) -> str:
        """TODO"""
        return self._filepath

    def get_charset(self) -> str:
        """TODO"""
        return self._charset.value
