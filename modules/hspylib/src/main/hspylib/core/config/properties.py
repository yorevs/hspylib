#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.config
      @file: properties.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from collections import defaultdict
from hspylib.core.config.parser_factory import ParserFactory
from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import dirname, run_dir, touch_file
from hspylib.core.tools.text_tools import environ_name
from os.path import basename
from typing import Any, Callable, Iterator, List, Optional, Type

import logging as log
import os

CONVERSION_FN = Type | Callable[[Any], Any]


class Properties:
    """The Properties class represents a persistent set of properties. Each key and its corresponding value in the
    property list is a string."""

    _default_name: str = "application"
    _default_ext: str = ".properties"

    @staticmethod
    def read_properties(filepath: str) -> "Properties":
        """Create properties based on absolute existing file path.
        :param filepath: the path of the file containing the properties
        """
        return Properties(load_dir=dirname(filepath), filename=basename(filepath))

    def __init__(self, filename: str = None, profile: str | None = None, load_dir: str | None = None) -> None:
        self._filename, self._extension = os.path.splitext(
            filename if filename else f"{self._default_name}{self._default_ext}"
        )
        self._profile = profile if profile else os.environ.get("ACTIVE_PROFILE", "")
        self._properties = defaultdict()
        self._load(load_dir or f"{run_dir()}/resources")

    def __str__(self) -> str:
        str_val = ""
        for key, value in self._properties.items():
            str_val += "{}{}={}".format("\n" if str_val else "", key, value)
        return str_val

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, item: str) -> Optional[Any]:
        return self.get(item)

    def __iter__(self) -> Iterator:
        return self._properties.__iter__()

    def __len__(self) -> int:
        """Retrieve the amount of properties"""
        return len(self._properties)

    def get(self, prop_name: str, cb_to_type: CONVERSION_FN = str, default: Any | None = None) -> Optional[Any]:
        """Retrieve a property specified by property and cast to the proper type. If the property is not found,
        return the default value."""

        try:
            value = self._get(prop_name)
            return cb_to_type(value) if value else None
        except TypeError:
            log.warning("Unable to convert property '%s' into '%s'", prop_name, cb_to_type)
            return default

    @property
    def as_dict(self) -> dict:
        return self._properties

    @property
    def values(self) -> List[Any]:
        """Retrieve all values for all properties"""
        return list(self._properties.values())

    @property
    def keys(self) -> List[str]:
        """Retrieve all values for all properties"""
        return list(self._properties.keys())

    @property
    def size(self) -> int:
        """Retrieve the amount of properties actually store."""
        return len(self._properties)

    def _get(self, key: str, default: Any = None) -> Optional[Any]:
        """Get a property value as string or default_value if the property was not found"""
        if value := os.environ.get(environ_name(key), None):
            return value
        return self._properties[key] if key in self._properties else default

    def _load(self, load_dir: str) -> None:
        """Read all properties from the file"""
        filepath = self._build_path(load_dir)
        if os.path.exists(filepath):
            return self._parse(filepath)

        raise FileNotFoundError(f'File "{filepath}" does not exist')

    def _build_path(self, load_dir: str) -> str:
        """Find the proper path for the properties file"""
        return f"{load_dir}/{self._filename}{'-' + self._profile if self._profile else ''}{self._extension}"

    def _parse(self, filepath: str) -> None:
        """Parse the properties file according to it's extension"""
        if not os.path.isfile(filepath):
            touch_file(filepath)
        ext = self._extension.lower()
        with open(filepath, encoding=Charset.UTF_8.val) as fh_props:
            parser = ParserFactory.create(ext)
            self._properties.update(parser.parse(fh_props))
        log.debug("Successfully loaded %d properties from: %s", len(self._properties), filepath)
