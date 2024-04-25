#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.config
      @file: path_object.py
   @created: Wed, 10 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/askai
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright (c) 2024, HomeSetup
"""

import json
import os
from dataclasses import dataclass
from os.path import expandvars, relpath, join
from pathlib import Path
from typing import Literal, Optional

from hspylib.core.metaclass.classpath import AnyPath


@dataclass(frozen=True)
class PathObject:
    """Dataclass that represents a system path. '~' and system variables are already resolved."""

    abs_dir: str
    rel_dir: str
    filename: str
    exists: bool
    kind: Literal["file", "folder"]

    @staticmethod
    def of(path_name: AnyPath) -> Optional['PathObject']:
        """Create a path object from a any path."""
        if path_name:
            path_dir: Path = Path(path_name) if isinstance(path_name, str) else path_name
            posix_path = Path(expandvars(path_dir.expanduser())).absolute()
            dir_name, filename = os.path.split(posix_path)
            if posix_path.exists() and posix_path.is_dir():
                dir_name = f"{dir_name}/{filename}"
                filename = ''
            if dir_name in ['.', '..', '']:
                dir_name = (dir_name or '.') + os.path.sep
            return PathObject(
                dir_name.strip(), relpath(dir_name, os.curdir), filename.strip(),
                posix_path.exists(), "folder" if posix_path.is_dir() else "file"
            )
        return None

    @staticmethod
    def split(path_name: AnyPath) -> tuple[str, str]:
        """Split any path into directory and file name."""
        po = PathObject.of(path_name)
        return po.abs_dir, po.filename

    def __str__(self) -> str:
        return self.join()

    def to_string(self) -> str:
        return f"PathObject: {json.dumps(self.__dict__, default=lambda obj: obj.__dict__)}"

    def join(self) -> str:
        """Split the path into directory and file names."""
        return join(self.abs_dir, self.filename)

    @property
    def is_dir(self) -> bool:
        return self.kind == 'folder'

    @property
    def is_file(self) -> bool:
        return self.kind == 'file'
