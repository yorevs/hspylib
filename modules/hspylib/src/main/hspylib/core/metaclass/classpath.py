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
import logging as log
import os
from pathlib import Path
from textwrap import dedent
from typing import Optional

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
    def log_dir(cls) -> Path:
        """TODO"""
        return cls.INSTANCE._log_dir

    @classmethod
    def list_resources(cls, directory: str | Path) -> str:
        """TODO"""
        res_str = Classpath.list_files(directory)
        for root, dirs, _ in os.walk(directory):
            for dirname in dirs:
                res_str += '  |-' + dirname + os.linesep
                res_str += cls.list_resources(os.path.join(root, dirname))
        return res_str

    @staticmethod
    def list_files(directory: str | Path) -> str:
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
    def get_resource_path(cls, resource: str | Path) -> Path:
        """TODO"""
        resource = Path(f'{cls.INSTANCE.resource_dir()}/{str(resource)}')
        if not resource.exists():
            raise ResourceNotFoundError(f'Resource {str(resource)} was not found!')
        return resource

    @classmethod
    def get_source_path(cls, source: str | Path) -> Path:
        """TODO"""
        filepath = Path(f"{cls.INSTANCE.source_root()}/{str(source)}")
        if not filepath.exists():
            raise SourceNotFoundError(f"Source {str(source)} was not found!")
        return filepath

    @classmethod
    def load_envs(cls, prefix: str = 'env', suffix: str = None, load_dir: str = None) -> None:
        """TODO"""
        env_file = f"{load_dir or f'{cls.INSTANCE.source_root()}/env'}/{prefix}{f'-{suffix}' if suffix else ''}.env"
        if os.path.exists(env_file):
            log.debug(f"ENVIRON::Loading environment file '{env_file}'")
            with open(env_file, 'r') as f_env:
                lines = f_env.readlines()
                lines = list(filter(lambda l: l.startswith('export '), filter(None, lines)))
                variables = list(map(lambda x: x.split('=', 1), map(lambda l: l[7:].strip(), lines)))
                for v in variables:
                    log.debug(f"ENVIRON::With environment variable\t'{v[0]}'")
                    os.environ[v[0]] = v[1]
        else:
            log.warning(f"ENVIRON::Environment file '{env_file}' was not found!")

    def __str__(self):
        return dedent(f"""
        |-source-root: {self._source_root}
        |-run-dir: {self.run_dir}
        |-resource-dir: {self._resource_dir}
        |-log-dir: {self._log_dir}
        """) + self.list_resources(self._resource_dir)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    Classpath.load_envs(
        suffix='stage',
        load_dir='/Users/hjunior/GIT-Repository/GAP/SBS/LIProductionalisationScripts/astra-db-atp-hydration/env')
