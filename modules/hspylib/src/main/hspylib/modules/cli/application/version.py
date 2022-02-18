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

   Copyright 2021, HSPyLib team
"""
import os
from typing import Tuple

from hspylib.core.tools.commons import read_version


class AppVersion:

    @staticmethod
    def load(filepath: str = None) -> 'AppVersion':
        if filepath and not os.path.exists(filepath):
            raise FileNotFoundError(
                f'File "{filepath}" does not exist')
        version = read_version(filepath or f"{os.getcwd()}/.version")
        return AppVersion(version)

    def __init__(self, version: Tuple[int, int, int]):
        self.version = version
        self.version_string = '.'.join(map(str, version))

    def __str__(self):
        return self.version_string

    def __repr__(self):
        return str(self)
