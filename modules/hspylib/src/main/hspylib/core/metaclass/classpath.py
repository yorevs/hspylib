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
from hspylib.core.tools.preconditions import check_state


class Classpath(metaclass=Singleton):
    """TODO"""

    def __init__(self, source_root: Path, run_dir: Path, resource_dir: Optional[Path]):
        check_state(
            source_root.exists()
            and run_dir.exists(),
            "source_root / run_dir are mandatory and must exist")
        self.source_root = source_root
        self.resource_dir = resource_dir
        self.run_dir = run_dir
        self.log_dir = os.getenv('LOG_DIR', self.run_dir)

    @classmethod
    def list_resources(cls, directory: Union[Path, str]) -> str:
        """TODO"""
        res_str = cls.list_files(directory)
        for root, dirs, _ in os.walk(directory):
            for dirname in dirs:
                res_str += '  |-' + dirname + os.linesep
                res_str += cls.list_resources(os.path.join(root, dirname))
        return res_str

    @classmethod
    def list_files(cls, directory: Union[Path, str]) -> str:
        """TODO"""
        res_str = ''
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                res_str += '    |-' + str(filename) + os.linesep
        return res_str

    @classmethod
    def source_root(cls) -> Path:
        """TODO"""
        return cls.INSTANCE.source_root

    @classmethod
    def run_dir(cls) -> Path:
        """TODO"""
        return cls.INSTANCE.run_dir

    @classmethod
    def resource_dir(cls) -> Path:
        """TODO"""
        return cls.INSTANCE.resource_dir

    @classmethod
    def log_dir(cls) -> Optional[Path]:
        """TODO"""
        return cls.INSTANCE.log_dir

    @classmethod
    def get_resource(cls, resource_path: Union[str, Path]) -> Path:
        """TODO"""
        resource = Path(f'{cls.INSTANCE.resource_dir}/{str(resource_path)}')
        if not resource.exists():
            raise ResourceNotFoundError(f'Resource {str(resource_path)} was not found!')
        return resource

    @classmethod
    def get_source(cls, source_path: Union[str, Path]) -> Path:
        """TODO"""
        source_path = Path(f'{cls.INSTANCE.source_root}/{str(source_path)}')
        if not source_path.exists():
            raise SourceNotFoundError(f'Source {str(source_path)} was not found!')
        return source_path

    def __str__(self):
        return dedent(f"""
        |-run-dir: {self.run_dir}
        |-source-root: {self.source_root}
        |-resources: {self.resource_dir}
        |-log_dir: {self.log_dir}
        """) + self.list_resources(self.resource_dir)

    def __repr__(self):
        return str(self)
