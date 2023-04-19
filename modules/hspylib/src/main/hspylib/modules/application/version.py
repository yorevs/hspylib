#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.application
      @file: version.py
   @created: Thu, 14 Feb 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from hspylib.core.enums.charset import Charset
from hspylib.core.preconditions import check_argument
from pathlib import Path
from typing import Union

import logging as log
import os
import re


class Version:
    """
    Ref.: https://semver.org/
    """

    @staticmethod
    def initial() -> "Version":
        return Version(0, 1, 0)

    @staticmethod
    def unversioned() -> "Version":
        return Version(-1, -1, -1)

    @staticmethod
    def load(filename: str = ".version", load_dir: Union[str, Path] = os.getcwd()) -> "Version":
        """Load a version from file."""
        filepath = f"{str(load_dir)}/{filename}"
        if not os.path.exists(filepath):
            log.warning('File "%s" does not exist. Could not fetch application version from %s', filepath, load_dir)
            return Version.unversioned()
        return Version._read(filepath)

    @staticmethod
    def _read(filepath: str = ".version") -> "Version":
        """Retrieve the version from the version file."""
        log.debug("Reading version from %s", filepath)
        with open(filepath, encoding=Charset.UTF_8.val) as fh_version:
            ver_str = fh_version.read().strip()
            if mat := re.search(r"v?((\d+)\.(\d+)\.(\d+)(.*))", ver_str):
                delimiters = re.findall(r"[-_ ]", ver_str)
                extras = re.split(r"[-_ ]", ver_str)[1:]
                ext = list(map("".join, zip(delimiters, extras)))
                return Version(mat.group(2), mat.group(3), mat.group(4), *ext)
            return Version.unversioned()

    def __init__(self, *args) -> None:
        """Application version. Additional labels for pre-release and build metadata are available as extensions
        to the MAJOR.MINOR.PATCH format:
            - MAJOR version when you make incompatible API changes
            - MINOR version when you add functionality in a backwards compatible manner
            - PATCH version when you make backwards compatible bug fixes
        :param version: The version number according to the following: MAJOR.MINOR.PATCH
        """
        check_argument(args and len(args) >= 3, "Version must have at least MAJOR.MINOR.PATCH numbers")
        self._major = args[0]
        self._minor = args[1]
        self._patch = args[2]
        self._ext = "".join(args[3:])
        self._version_string = f"{'.'.join(map(str, args[:3]))}{self._ext}"

    def __str__(self) -> str:
        return self._version_string

    def __repr__(self) -> str:
        return str(self)

    @property
    def version(self) -> str:
        """TODO"""
        return f"v{str(self)}"
