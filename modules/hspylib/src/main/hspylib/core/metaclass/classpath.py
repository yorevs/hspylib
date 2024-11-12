#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: hspylib
   @package: hspylib.core.metaclass
      @file: __classpath__.py
   @created: Wed, 8 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import logging as log
import os
from pathlib import Path
from textwrap import dedent
from types import NoneType
from typing import Optional, TypeAlias, Union

from hspylib.core.enums.charset import Charset
from hspylib.core.preconditions import check_argument, check_not_none, check_state

AnyPath: TypeAlias = Union[Path, str, NoneType]


class Classpath:
    """The classpath tells Python applications where to look in the filesystem for source and resource files."""

    def __init__(
        self,
        source_dir: AnyPath = None,
        root_dir: AnyPath = None,
        resource_dir: AnyPath = None
    ):

        if source_dir:
            check_state(Path(source_dir).exists(), f"Source dir does not exist: '{source_dir}'")
        if root_dir:
            check_state(Path(root_dir).exists(), f"Root dir does not exist: '{root_dir}'")

        self.source_root = Path(os.getenv("SOURCE_ROOT", str(source_dir or os.curdir)))
        self.root_dir = Path(str(root_dir or self.source_root))
        self.resource_dir = Path(str(resource_dir or f"{self.source_root}/resources"))
        self.log_dir = Path(os.getenv("HHS_LOG_DIR", f"{self.root_dir}/log") or self.root_dir)

    @property
    def source_path(self) -> Path:
        """Return the source directory of the module."""
        return self.source_root

    @property
    def run_path(self) -> Path:
        """Return the running path of the module."""
        return self.root_dir

    @property
    def resource_path(self) -> Path:
        """Return the resources directory of the module."""
        return self.resource_dir

    @property
    def log_path(self) -> Path:
        """Return the directory where the module logs are stored."""
        return self.log_dir

    @property
    def list_resources(self) -> Optional[str]:
        """Walk through the resources directory and display all resource files.
        :return: A string representation of the list of resource files found, or None if no files are found
        """
        def list_resources_closure(directory: str | Path, depth: int = 4) -> Optional[str]:
            """Recursively list the resources"""
            if os.path.exists(directory):
                res_str = self.list_files(directory, depth)
                for root, dirs, _ in os.walk(directory):
                    for dir_name in dirs:
                        res_str += " " * depth + "|-" + dir_name + os.linesep
                        res_str += list_resources_closure(os.path.join(root, dir_name), depth + 2) or ""
                return res_str
            return None

        return list_resources_closure(self.resource_path)

    @staticmethod
    def list_files(directory: AnyPath, depth: int = 4) -> str:
        """Walk through the specified directory up to a certain depth and build a list of all files.
        :param directory: The directory path to start the file listing from.
        :param depth: The maximum depth to traverse within the directory, default is 4.
        :return: A string representation of the list of files found.
        """
        res_str = ""
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                if os.path.isfile(f):
                    res_str += " " * depth + "|-" + str(filename) + os.linesep
        return res_str

    def get_resource(self, resource: AnyPath) -> Path:
        """Return the path of the given resource.
        :param resource: The name or path of the resource to locate.
        :return: The path object of the specified resource.
        :raises FileNotFoundError: if the resource file is not found.
        """
        check_not_none(resource, "Must provide a valid resource path")
        if not (resource := Path(f"{self.resource_path}/{str(resource)}")).exists():
            raise FileNotFoundError(f"Resource {str(resource)} was not found at: '{self.source_path}' !")
        return resource

    def get_source(self, source: AnyPath) -> Path:
        """Return the path of the given source file.
        :param source: The name or path of the source file to locate
        :return: The path object of the specified source file
        :raises FileNotFoundError: if the source file is not found.
        """
        check_not_none(source, "Must provide a valid source path")
        if not (filepath := Path(f"{self.source_path}/{str(source)}")).exists():
            raise FileNotFoundError(f"Source {str(source)} was not found at: '{self.source_path}' !")
        return filepath

    def load_envs(
        self,
        prefix: str | None = None,
        suffix: str | None = None,
        load_dir: str | None = None,
        raise_error: bool = False,
    ) -> None:
        """Load environment variables from an environment file.
        :param prefix: Optional prefix to filter environment variables
        :param suffix: Optional suffix to filter environment variables
        :param load_dir: Optional directory to load the environment file from
        :param raise_error: If True, raises an error if loading fails
        :raises FileNotFoundError: if the environment file is not found and raise_error is True
        """
        load_path = Path(load_dir or f"{self.source_path}/env")
        check_argument(load_path.exists(), f"Load path does not exist: '{load_path}'!")
        files = [f"{load_path}/{prefix or ''}{f'-{suffix}' if suffix else '.env'}", f"{load_path}/.envrc"]

        if env_file := next((f for f in files if os.path.exists(f)), None):
            log.debug("ENVIRONMENT::Loading environment file '%s'", env_file)
            with open(env_file, "r", encoding=Charset.UTF_8.val) as f_env:
                lines = list(filter(lambda line: line.startswith("export "), filter(None, f_env.readlines())))
                variables = list(map(lambda x: x.split("=", 1), map(lambda var: var[7:].strip(), lines)))
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
          |-source-root: {self.source_path}
          |-run-dir: {self.root_dir}
          |-log-dir: {self.log_path}
          |-resource-dir: {self.resource_path}
        """
            )
            + f"{self.list_resources or ''})"
        )

    def __repr__(self):
        return str(self)
