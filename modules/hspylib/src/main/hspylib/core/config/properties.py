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
from configparser import ConfigParser
from typing import List, Optional

import yaml

from hspylib.core.tools.commons import flatten_dict, run_dir, str_to_bool, touch_file


class Properties:
    """TODO"""

    _default_name = 'application'
    _default_extension = '.properties'
    _profiled_format = '{}-{}{}'
    _simple_format = '{}{}'

    @staticmethod
    def environ_name(property_name: str) -> str:
        """Retrieve the environment name of the specified property name
        :param property_name: the name of the property using space, dot or dash notations
        """
        return re.sub('[ -.]', '_', property_name).upper()

    @staticmethod
    def read_properties(all_lines: List[str]) -> dict:
        return {
            p[0].strip(): p[1].strip() for p in [
                p.split('=', 1) for p in list(
                    filter(lambda l: re.match('[a-zA-Z0-9][._\\-a-zA-Z0-9]* *=.*', l), all_lines)
                )
            ]
        }

    @staticmethod
    def read_cfg_or_ini(all_lines: List[str]):
        string = os.linesep.join(all_lines)
        all_cfgs = {}
        cfg = ConfigParser()
        cfg.read_string(string)
        for section in cfg.sections():
            all_cfgs.update(dict(cfg.items(section)))
        return all_cfgs

    def __init__(self, filename: str = None, profile: str = None, load_dir: str = None):

        filename, extension = os.path.splitext(
            filename if filename else f'{self._default_name}{self._default_extension}')

        self.filename = filename
        self.extension = extension
        self.profile = profile if profile else os.environ.get('ACTIVE_PROFILE')
        self.load_dir = load_dir if load_dir else f'{run_dir()}/resources'
        self.filepath = None
        self.properties = {}
        self._read()

    def __str__(self):
        str_val = ''
        for key, value in self.properties.items():
            str_val += '{}{}={}'.format('\n' if str_val else '', key, value)
        return str_val

    def __getitem__(self, item: str):
        return self.get(item)

    def __iter__(self):
        return self.properties.__iter__()

    def __len__(self) -> int:
        """Retrieve the amount of properties"""
        return len(self.properties) if self.properties else 0

    def get(self, key: str, default_value=None) -> Optional[str]:
        """Get a property value as string or default_value if the property was not found"""
        return self.properties[key.strip()] if key.strip() in self.properties else default_value

    def get_int(self, key: str, default_value=None) -> Optional[int]:
        """Get and convert a property value into int or return a default value if any error occurred"""
        try:
            return int(self.get(key))
        except TypeError:
            return default_value

    def get_float(self, key: str, default_value=None) -> Optional[float]:
        """Get and convert a property value into float or return a default value if any error occurred"""
        try:
            return float(self.get(key))
        except TypeError:
            return default_value

    def get_bool(self, key: str, default_value=None) -> Optional[bool]:
        """Get and convert a property value into bool or return a default value if any error occurred"""
        try:
            return str_to_bool(self.get(key).lower())
        except TypeError:
            return default_value

    def values(self) -> list:
        """Retrieve all values for all properties"""
        return list(self.properties.values())

    def _read(self) -> None:
        """Read all properties from the file"""
        self.filepath = self._find_path()
        if os.path.exists(self.filepath):
            self._parse()
        else:
            raise FileNotFoundError(
                f'File "{self.filepath}" does not exist')

    def _find_path(self) -> str:
        """Find the proper path for the properties file"""
        if self.profile:
            filepath = self._profiled_format \
                .format(self.filename, self.profile, self.extension)
        else:
            filepath = self._simple_format \
                .format(self.filename, self.extension)
        return f'{self.load_dir}/{filepath}'

    def _parse(self) -> None:
        """Parse the properties file according to it's extension"""
        if not os.path.isfile(self._find_path()):
            touch_file(self._find_path())
        with open(self.filepath, encoding='utf-8') as fh_props:
            if self.extension in ['.ini', '.cfg']:
                all_lines = list(map(str.strip, filter(None, fh_props.readlines())))
                self.properties.update(self.read_cfg_or_ini(all_lines))
            elif self.extension == '.properties':
                all_lines = list(map(str.strip, filter(None, fh_props.readlines())))
                self.properties.update(self.read_properties(all_lines))
            elif self.extension in ['.yml', '.yaml']:
                self.properties.update(flatten_dict(yaml.safe_load(fh_props)))
            else:
                raise NotImplementedError(f'Extension {self.extension} is not supported')
        log.info('Successfully loaded %d properties from:\n\t=>%s', len(self.properties), self.filepath)
