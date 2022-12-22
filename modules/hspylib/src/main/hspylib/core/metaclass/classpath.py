#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
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

from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import ResourceNotFoundError, SourceNotFoundError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_argument, check_not_none, check_state

AnyPath = Path | str | None


class Classpath(metaclass=Singleton):
    """The classpath tells Python applications where to look in the filesystem for source and resource files."""

    INSTANCE = None

    def __init__(self, source_root: AnyPath = None, run_dir: AnyPath = None, resource_dir: AnyPath = None):

        if source_root:
            check_state(Path(str(source_root)).exists(), "source_root must exist")
        if run_dir:
            check_state(Path(str(run_dir)).exists(), "run_dir must exist")

        self.source_root = Path(os.getenv("SOURCE_ROOT", str(source_root or os.curdir)))
        self.run_dir = Path(str(run_dir or self.source_root))
        self.resource_dir = Path(str(resource_dir or f"{self.source_root}/resources"))
        self.log_dir = Path(os.getenv("LOG_DIR", f"{self.run_dir}/log") or self.run_dir)

    @classmethod
    def source_path(cls) -> Path:
        """TODO"""
        return cls.INSTANCE.source_root

    @classmethod
    def run_path(cls) -> Path:
        """TODO"""
        return cls.INSTANCE.run_dir

    @classmethod
    def resource_path(cls) -> Path:
        """TODO"""
        return cls.INSTANCE.resource_dir

    @classmethod
    def log_path(cls) -> Path:
        """TODO"""
        return cls.INSTANCE.log_dir

    @classmethod
    def list_resources(cls) -> str:
        def list_resources_closure(directory: str | Path, depth: int = 4) -> Optional[str]:
            """Walk through resources directory and build a list with all files"""
            if os.path.exists(directory):
                res_str = Classpath._list_files(directory, depth)
                for root, dirs, _ in os.walk(directory):
                    for dirname in dirs:
                        res_str += " " * depth + "|-" + dirname + os.linesep
                        res_str += list_resources_closure(os.path.join(root, dirname), depth + 2) or ""
                return res_str
            return None

        return list_resources_closure(cls.resource_path())

    @staticmethod
    def _list_files(directory: str | Path, depth: int = 4) -> str:
        """Walk through directory and build a list with all files"""
        res_str = ""
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                if os.path.isfile(f):
                    res_str += " " * depth + "|-" + str(filename) + os.linesep
        return res_str

    @classmethod
    def get_resource_path(cls, resource: str | Path) -> Path:
        """Return the path of the given resource"""
        check_not_none(resource, "Must provide a valid resource path")
        resource = Path(f"{cls.resource_path()}/{str(resource)}")
        if not resource.exists():
            raise ResourceNotFoundError(f"Resource {str(resource)} was not found at {cls.INSTANCE.source_path()}!")
        return resource

    @classmethod
    def get_source_path(cls, source: str | Path) -> Path:
        """Return the path of the given source"""
        check_not_none(source, "Must provide a valid source path")
        filepath = Path(f"{cls.source_path()}/{str(source)}")
        if not filepath.exists():
            raise SourceNotFoundError(f"Source {str(source)} was not found at {cls.INSTANCE.source_path()}!")
        return filepath

    @classmethod
    def load_envs(
        cls,
        prefix: str | None = None,
        suffix: str | None = None,
        load_dir: str | None = None,
        raise_error: bool = False,
    ) -> None:
        """Load environment variables from environment file."""

        load_path = Path(load_dir or f"{cls.source_path()}/env")
        check_argument(load_path.exists())
        files = [f"{load_path}/{prefix or ''}{f'-{suffix}' if suffix else '.env'}", f"{load_path}/.envrc"]
        env_file = next((f for f in files if os.path.exists(f)), None)
        if env_file:
            log.debug("ENVIRONMENT::Loading environment file '%s'", env_file)
            with open(env_file, "r", encoding=Charset.UTF_8.val) as f_env:
                lines = f_env.readlines()
                lines = list(filter(lambda l: l.startswith("export "), filter(None, lines)))
                variables = list(map(lambda x: x.split("=", 1), map(lambda l: l[7:].strip(), lines)))
                for v in variables:
                    log.debug("ENVIRONMENT::Setting environment variable\t'%s'", v[0])
                    os.environ[v[0]] = v[1]
        else:
            if raise_error:
                raise FileNotFoundError(f"None of the environment files: {files} were found!")
            log.warning("ENVIRONMENT::None of the environment files: %s were found", files)

    def __str__(self) -> str:
        return (
            dedent(
                f"""
        Classpath(
          |-cur-working-dir: {os.getcwd()}
          |-source-root: {self.source_path()}
          |-run-dir: {self.run_dir}
          |-log-dir: {self.log_path()}
          |-resource-dir: {self.resource_path()}
        """
            )
            + f"{self.list_resources() or ''})"
        )

    def __repr__(self):
        return str(self)
