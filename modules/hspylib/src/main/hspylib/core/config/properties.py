#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.core.config
      @file: properties.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import logging as log
import os
import re
from collections import defaultdict
from configparser import ConfigParser
from typing import Any, Callable, Iterator, List, Optional, Type, Dict, TextIO

import toml
import yaml

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import run_dir, touch_file
from hspylib.core.tools.dict_tools import flatten_dict

CONVERSION_FN = Type | Callable[[Any], Any]


class Properties:
    """The Properties class represents a persistent set of properties. Each key and its corresponding value in the
    property list is a string."""

    _default_name: str = "application"
    _default_ext: str = ".properties"

    @staticmethod
    def environ_name(property_name: str) -> str:
        """Retrieve the environment name of the specified property name
        :param property_name: the name of the property using space, dot or dash notations
        """
        return re.sub("[ -.]", "_", property_name).upper()

    @staticmethod
    def read_properties(file_handler: TextIO) -> Dict[str, Any]:
        """Reads properties from properties file (key and element pairs) from the input list."""
        all_lines = list(map(str.strip, filter(None, file_handler.readlines())))
        # fmt: off
        return {
            p[0].strip(): p[1].strip()
            for p in [
                p.split("=", 1) for p in list(
                    filter(lambda l: re.match(r"[a-zA-Z]([.\\-]|\w)* *= *.+", l), all_lines)
                )
            ]
        }
        # fmt: off

    @staticmethod
    def read_cfg_or_ini(file_handler: TextIO) -> Dict[str, Any]:
        """Reads properties from a cfg or ini file (key and element pairs) from the input list."""
        all_lines = list(map(str.strip, filter(None, file_handler.readlines())))
        string = os.linesep.join(all_lines)
        all_cfgs = {}
        cfg = ConfigParser()
        cfg.read_string(string)
        for section in cfg.sections():
            all_cfgs.update(dict(cfg.items(section)))
        return all_cfgs

    @staticmethod
    def read_yaml(file_handler: TextIO) -> Dict[str, Any]:
        """Reads properties from a yaml file (key and element pairs) from the input list."""
        return flatten_dict(yaml.safe_load(file_handler))

    @staticmethod
    def read_toml(file_handler: TextIO) -> Dict[str, Any]:
        """Reads properties from a toml file (key and element pairs) from the input list."""
        return flatten_dict(toml.load(file_handler))

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
        if value := os.environ.get(self.environ_name(key), None):
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
            if ext in [".ini", ".cfg"]:
                all_properties = self.read_cfg_or_ini(fh_props)
            elif ext == ".properties":
                all_properties = self.read_properties(fh_props)
            elif ext in [".yml", ".yaml"]:
                all_properties = self.read_yaml(fh_props)
            elif ext == ".toml":
                all_properties = self.read_toml(fh_props)
            else:
                raise NotImplementedError(f"Extension {ext} is not supported")
            self._properties.update(all_properties)
        log.debug("Successfully loaded %d properties from: %s", len(self._properties), filepath)
