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
from pathlib import Path
from typing import Tuple, Union

from hspylib.core.tools.commons import read_version


class Version:

    @staticmethod
    def load(filename: str = '.version', load_dir: Union[str, Path] = os.getcwd()) -> 'Version':
        filepath = f'{str(load_dir)}/{filename}'
        if not os.path.exists(filepath):
            log.warning('File "%s" does not exist. Could not fetch application version', filepath)
            return Version((0, 0, 0))

        return Version(read_version(filepath))

    def __init__(self, version: Tuple[int, int, int]):
        self.version = version
        self.version_string = '.'.join(map(str, version))

    def __str__(self):
        return self.version_string

    def __repr__(self):
        return str(self)

    def version(self) -> str:
        """TODO"""
        return f'v{str(self)}'
