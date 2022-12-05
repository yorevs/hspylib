#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.application
      @file: version.py
   @created: Thu, 14 Feb 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import logging as log
import os
import re
from pathlib import Path
from typing import Tuple, Union

from hspylib.core.enums.charset import Charset


class Version:

    @staticmethod
    def load(filename: str = '.version', load_dir: Union[str, Path] = os.getcwd()) -> 'Version':
        """Load a version from file in the form: [major.minor.build] ."""
        filepath = f'{str(load_dir)}/{filename}'
        if not os.path.exists(filepath):
            log.warning('File "%s" does not exist. Could not fetch application version', filepath)
            return Version((-1, -1, -1))

        return Version(Version.read(filepath))

    @staticmethod
    def read(filepath: str = ".version") -> Tuple[int, int, int]:
        """Retrieve the version from the version file in the form: [major.minor.build] ."""
        try:
            log.debug("Reading version from %s", filepath)
            with open(filepath, encoding=Charset.UTF_8.val) as fh_version:
                ver = tuple(map(int, map(str.strip, fh_version.read().split('.'))))
                return ver if ver and re.search(r'(\d+, \d+, \d+)', str(ver)) else (-1, -1, -1)
        except FileNotFoundError:
            return -1, -1, -1

    def __init__(self, version: Tuple[int, int, int]):
        self._version = version
        self._version_string = '.'.join(map(str, version))

    def __str__(self):
        return self._version_string

    def __repr__(self):
        return str(self)

    @property
    def version(self) -> str:
        """TODO"""
        return f'v{str(self)}'
