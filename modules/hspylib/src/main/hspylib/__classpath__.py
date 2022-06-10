#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib
   @package: hspylib.main.hspylib
      @file: __classpath__.py
   @created: Wed, 8 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import os
from pathlib import Path
from textwrap import dedent
from typing import Union

from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import get_path, run_dir


class Classpath(metaclass=Singleton):
    """TODO"""

    # Location of the running dir
    RUN_DIR = get_path(run_dir())

    # Location of the source root
    SOURCE_ROOT = get_path(__file__)

    # Location of the resources directory
    RESOURCE_DIR = (SOURCE_ROOT / "resources")

    @classmethod
    def _list_resources(cls, directory: Union[Path, str]) -> str:
        """TODO"""
        res_str = cls._list_files(directory)
        for root, dirs, files in os.walk(directory):
            for dirname in dirs:
                res_str += '  |-' + dirname + os.linesep
                res_str += cls._list_resources(os.path.join(root, dirname))
        return res_str

    @classmethod
    def _list_files(cls, directory: Union[Path, str]) -> str:
        """TODO"""
        res_str = ''
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                res_str += '    |-' + filename + os.linesep
        return res_str

    def __init__(self):
        pass

    def __str__(self):
        return dedent(f"""
        |-run-dir: {self.RUN_DIR}
        |-source-root: {self.SOURCE_ROOT}
        |-resources: {self.RESOURCE_DIR}
        """) + self._list_resources(self.RESOURCE_DIR)

    def __repr__(self):
        return str(self)

# Instantiate the classpath singleton
Classpath()

def get_resource(resource_path) -> Path:
    """TODO"""
    return Path(f'{Classpath.RESOURCE_DIR}/{resource_path}')

def get_source(source_path) -> Path:
    """TODO"""
    return Path(f'{Classpath.SOURCE_ROOT}/{source_path}')
