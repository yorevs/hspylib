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
from typing import Tuple

from hspylib.core.tools.commons import read_version


class AppVersion:

    @staticmethod
    def load(filename: str = '.version', load_dir: str = os.getcwd()) -> 'AppVersion':
        filepath = f'{load_dir}/{filename}'
        if not os.path.exists(filepath):
            log.warning(f'File "{filepath}" does not exist')
            return AppVersion((0, 0, 0))

        return AppVersion(read_version(filepath))

    def __init__(self, version: Tuple[int, int, int]):
        self.version = version
        self.version_string = '.'.join(map(str, version))

    def __str__(self):
        return self.version_string

    def __repr__(self):
        return str(self)
