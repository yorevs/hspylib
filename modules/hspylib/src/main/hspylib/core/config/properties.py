#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.config
      @file: properties.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

import logging as log
import os
from collections import defaultdict
from os.path import basename, expandvars
from typing import Any, Callable, Iterator, List, Optional, TypeAlias

from hspylib.core.config.parser_factory import ParserFactory
from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import PropertyError
from hspylib.core.metaclass.classpath import AnyPath
from hspylib.core.tools.commons import dirname, root_dir, touch_file
from hspylib.core.tools.text_tools import environ_name

ConversionFn: TypeAlias = Callable[[Any], Any]


class Properties:
    """The Properties class represents a persistent set of properties. Each key and its corresponding value in the
    property list is a string."""

    _default_name: str = "application"
    _default_ext: str = ".properties"

    @staticmethod
    def read_properties(filepath: AnyPath) -> "Properties":
        """Create properties based on absolute existing file path.
        :param filepath: the path of the file containing the properties
        """
        return Properties(load_dir=dirname(filepath), filename=basename(filepath))

    @staticmethod
    def convert_type(value: Any, cb_to_type: ConversionFn) -> Optional[Any]:
        """TODO"""
        try:
            return cb_to_type(value) if value else None
        except TypeError:
            raise PropertyError(f"Unable to convert value '{value}' into '{cb_to_type}'")

    def __init__(self, filename: str = None, profile: str | None = None, load_dir: str | None = None) -> None:
        self._filename, self._extension = os.path.splitext(
            filename if filename else f"{self._default_name}{self._default_ext}"
        )
        self._profile = profile if profile else os.environ.get("ACTIVE_PROFILE", "")
        self._properties = defaultdict()
        self._load(load_dir or f"{root_dir()}/resources")

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

    @property
    def as_dict(self) -> dict:
        return self._properties

    @property
    def values(self) -> List[Any]:
        """Retrieve all values for all properties."""
        return list(self._properties.values())

    @property
    def keys(self) -> List[str]:
        """Retrieve all values for all properties."""
        return list(self._properties.keys())

    @property
    def size(self) -> int:
        """Retrieve the amount of properties actually store."""
        return len(self._properties)

    def read_value(self, key: str, default: Any = None) -> Optional[Any]:
        """Get a property value as string or default_value if the property was not found.
        :param key: the property key name.
        :param default: a default value for the property case it is not found.
        """
        if value := os.environ.get(environ_name(key), None):
            return value
        return self._properties[key] if key in self._properties else default

    def get(self, key: str, cb_to_type: ConversionFn = str, default: Any | None = None) -> Optional[Any]:
        """Retrieve a property specified by property and cast to the proper type. If the property is not found,
        return the default value.
        :param key: the property key name.
        :param cb_to_type: the type conversion. Default is str().
        :param default: a default value for the property case it is not found.
        """
        return self.convert_type(self.read_value(key, default), cb_to_type)

    def _load(self, load_dir: AnyPath) -> None:
        """Read all properties from the file.
        :param load_dir: where the properties should be loaded from.
        """
        filepath: str = expandvars(self._build_path(str(load_dir)))
        if os.path.exists(filepath):
            return self._parse(filepath)

        raise FileNotFoundError(f'File "{filepath}" does not exist')

    def _build_path(self, load_dir: AnyPath) -> str:
        """Find the proper path for the properties file.
        :param load_dir: where the properties were be loaded from.
        """
        return f"{load_dir}/{self._filename}{'-' + self._profile if self._profile else ''}{self._extension}"

    def _parse(self, filepath: AnyPath) -> None:
        """Parse the properties file according to it's extension.
        :param filepath: the properties file path.
        """
        expanded_path: str = expandvars(str(filepath))
        if not os.path.isfile(expanded_path):
            touch_file(expanded_path)
        ext = self._extension.lower()
        with open(expanded_path, encoding=Charset.UTF_8.val) as fh_props:
            parser = ParserFactory.create(ext)
            self._properties.update(parser.parse(fh_props))
        log.debug("Successfully loaded %d properties from: %s", len(self._properties), expanded_path)
