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
from typing import Optional, Union

from hspylib.core.exception.exceptions import ResourceNotFoundError, SourceNotFoundError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_state


class Classpath(metaclass=Singleton):
    """The classpath tells Python applications where to look in the filesystem for source and resource files."""

    def __init__(
            self,
            source_root: Optional[Path] = None,
            run_dir: Optional[Path] = None,
            resource_dir: Optional[Path] = None):

        if source_root:
            check_state(source_root.exists(), "source_root must exist")
        if run_dir:
            check_state(run_dir.exists(), "run_dir must exist")
        self._source_root = Path(os.getenv('SOURCE_ROOT', source_root)) or Path(os.curdir)
        self._run_dir = run_dir or Path(os.curdir)
        self._resource_dir = resource_dir or Path(f"{self._source_root}/resources")
        self._log_dir = Path(os.getenv('LOG_DIR', f"{self._run_dir}/log"))

    @classmethod
    def source_root(cls) -> Path:
        """TODO"""
        return cls.INSTANCE._source_root

    @classmethod
    def run_dir(cls) -> Path:
        """TODO"""
        return cls.INSTANCE._run_dir

    @classmethod
    def resource_dir(cls) -> Path:
        """TODO"""
        return cls.INSTANCE._resource_dir

    @classmethod
    def log_dir(cls) -> Optional[Path]:
        """TODO"""
        return cls.INSTANCE._log_dir

    @classmethod
    def list_resources(cls, directory: Union[Path, str]) -> str:
        """TODO"""
        res_str = Classpath.list_files(directory)
        for root, dirs, _ in os.walk(directory):
            for dirname in dirs:
                res_str += '  |-' + dirname + os.linesep
                res_str += cls.list_resources(os.path.join(root, dirname))
        return res_str

    @staticmethod
    def list_files(directory: Union[Path, str]) -> str:
        """TODO"""
        res_str = ''
        if (isinstance(directory, str) and os.path.exists(directory)) \
            or (isinstance(directory, Path) and directory.exists()):
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                if os.path.isfile(f):
                    res_str += '    |-' + str(filename) + os.linesep
        return res_str

    @classmethod
    def get_resource_path(cls, resource_path: Union[str, Path]) -> Path:
        """TODO"""
        resource = Path(f'{cls.INSTANCE.resource_dir()}/{str(resource_path)}')
        if not resource.exists():
            raise ResourceNotFoundError(f'Resource {str(resource_path)} was not found!')
        return resource

    @classmethod
    def get_source_path(cls, source_path: Union[str, Path]) -> Path:
        """TODO"""
        filepath = Path(f"{cls.INSTANCE.source_root()}/{str(source_path)}")
        if not filepath.exists():
            raise SourceNotFoundError(f"Source {str(source_path)} was not found!")
        return filepath

    def __str__(self):
        return dedent(f"""
        |-run-dir: {self.run_dir}
        |-source-root: {self._source_root}
        |-resources: {self._resource_dir}
        |-log-dir: {self._log_dir}
        """) + self.list_resources(self._resource_dir)

    def __repr__(self):
        return str(self)
