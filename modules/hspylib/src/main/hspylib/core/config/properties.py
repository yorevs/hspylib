#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.config
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
from typing import Any, Callable, Iterator, List, Optional, Type

import yaml

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import flatten_dict, run_dir, touch_file


class Properties:
    """The Properties class represents a persistent set of properties. Each key and its corresponding value in the
    property list is a string."""

    _default_name = 'application'
    _default_extension = '.properties'

    @staticmethod
    def _environ_name(property_name: str) -> str:
        """Retrieve the environment name of the specified property name
        :param property_name: the name of the property using space, dot or dash notations
        """
        return re.sub('[ -.]', '_', property_name).upper()

    @staticmethod
    def _read_properties(all_lines: List[str]) -> dict:
        """Reads a property list (key and element pairs) from the input list."""
        return {
            p[0].strip(): p[1].strip() for p in [
                p.split('=', 1) for p in list(
                    filter(lambda l: re.match('[a-zA-Z\d][._\\-a-zA-Z\d]* *=.*', l), all_lines)
                )
            ]
        }

    @staticmethod
    def _read_cfg_or_ini(all_lines: List[str]):
        """Reads a cfg or ini list (key and element pairs) from the input list."""
        string = os.linesep.join(all_lines)
        all_cfgs = {}
        cfg = ConfigParser()
        cfg.read_string(string)
        for section in cfg.sections():
            all_cfgs.update(dict(cfg.items(section)))
        return all_cfgs

    def __init__(self, filename: str = None, profile: str = None, load_dir: str = None):

        self._filename, self._extension = os.path.splitext(
            filename if filename else f'{self._default_name}{self._default_extension}')
        self._profile = profile if profile else os.environ.get('ACTIVE_PROFILE', '')
        self._properties = defaultdict()
        self._load(load_dir or f'{run_dir()}/resources')

    def __str__(self) -> str:
        str_val = ''
        for key, value in self._properties.items():
            str_val += '{}{}={}'.format('\n' if str_val else '', key, value)
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

    def get(self, key: str, value_type: Type | Callable = str, default_value: Optional[str] = None) -> Optional[Any]:
        try:
            value = self._get(key)
            return value_type(value) if value else None
        except TypeError:
            return default_value

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

    def _get(self, key: str, default_value: Any = None) -> Optional[Any]:
        """Get a property value as string or default_value if the property was not found"""
        value = os.environ.get(self._environ_name(key), None)
        if value:
            return value
        return self._properties[key] if key in self._properties else default_value

    def _load(self, load_dir: str) -> None:
        """Read all properties from the file"""
        filepath = self._build_path(load_dir)
        if os.path.exists(filepath):
            return self._parse(filepath)

        raise FileNotFoundError(
            f'File "{filepath}" does not exist')

    def _build_path(self, load_dir: str) -> str:
        """Find the proper path for the properties file"""
        if self._profile:
            filepath = f'{load_dir}/{self._filename}-{self._profile}{self._extension}'
        else:
            filepath = f'{load_dir}/{self._filename}{self._extension}'

        return filepath

    def _parse(self, filepath: str) -> None:
        """Parse the properties file according to it's extension"""
        if not os.path.isfile(filepath):
            touch_file(filepath)
        ext = self._extension.lower()
        with open(filepath, encoding=str(Charset.UTF_8)) as fh_props:
            if ext in ['.ini', '.cfg']:
                all_lines = list(map(str.strip, filter(None, fh_props.readlines())))
                self._properties.update(self._read_cfg_or_ini(all_lines))
            elif ext == '.properties':
                all_lines = list(map(str.strip, filter(None, fh_props.readlines())))
                self._properties.update(self._read_properties(all_lines))
            elif ext in ['.yml', '.yaml']:
                self._properties.update(flatten_dict(yaml.safe_load(fh_props)))
            else:
                raise NotImplementedError(f'Extension {ext} is not supported')
        log.info('Successfully loaded %d properties from:\n\t=>%s', len(self._properties), filepath)
