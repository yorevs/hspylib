#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   Provides an engine to manage app versions
   @project: HSPyLib
   @package: hspylib.app._versioner.src.main
      @file: _versioner.py
   @created: Thu, 14 Nov 2019
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import fileinput
import logging as log
import os
import re
from typing import List, Optional

from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import run_dir
from hspylib.core.tools.preconditions import check_argument

from versioner.entity.version import Version
from versioner.enums.version_state import VersionState


class Versioner(metaclass=Singleton):
    """
        Labels:
            MAJOR version when you make incompatible API changes.
            MINOR version when you add functionality in a backwards compatible manner.
            PATCH version when you make backwards compatible bug fixes.

        @Additional labels for pre-release and build metadata are available as extensions to the
                    MAJOR.MINOR.PATCH format.

        Extensions:
            SNAPSHOT => STABLE => RELEASE
    """

    def __init__(self, initial_version: str, search_dir: str, files: List[str]):
        self._initial_version = initial_version
        self._version = Version.parse(initial_version)
        self._search_dir = search_dir or run_dir()
        self._files = self._assert_exist(files)

    def __str__(self):
        return str(self._version)

    def __repr__(self):
        return str(self)

    def promote(self) -> Version:
        """ Promote the current version in the order: DEVELOPMENT->SNAPSHOT->STABLE->RELEASE """
        if self._assert_extension():
            if self._version.state and self._version.state != VersionState.RELEASE:
                self._version.state = VersionState.of_value(
                    min(VersionState.RELEASE.value, self._version.state.value << 1))
                log.debug(f"Version has been promoted to {self._version}")
            else:
                log.error(f"Version  {self._version} can't be promoted")

        return self._version

    def demote(self) -> Version:
        """ Demote the current version in the order: RELEASE->STABLE->SNAPSHOT->DEVELOPMENT """
        if self._assert_extension():
            if self._version.state and self._version.state != VersionState.DEVELOPMENT:
                self._version.state = VersionState.of_value(
                    max(VersionState.DEVELOPMENT.value, self._version.state.value >> 1))
                log.debug(f"Version has been demoted to {self._version}")
            else:
                log.error(f"Version  {self._version} can't be demoted")
        return self._version

    def major(self) -> Version:
        """ Update current major part of the version """
        self._version.major += 1
        self._version.minor = 0
        self._version.patch = 0
        self._version.state = VersionState.DEVELOPMENT if self._version.state else None
        log.debug(f"Major has increased to {self._version} (Major)")
        return self._version

    def minor(self) -> Version:
        """ Update current minor part of the version """
        self._version.minor += 1
        self._version.patch = 0
        self._version.state = VersionState.DEVELOPMENT if self._version.state else None
        log.debug(f"Minor has increased to {self._version} (Minor)")
        return self._version

    def patch(self) -> Version:
        """ Update current patch part of the version """
        self._version.patch += 1
        self._version.state = VersionState.DEVELOPMENT if self._version.state else None
        log.debug(f"Patch has increased to {self._version} (Patch)")
        return self._version

    def version(self) -> str:
        return str(self._version)

    def save(self, backup: str = None) -> Optional[List[str]]:
        """ Save the current version to the specified files and create a backup of the original files """
        changed_lines = []
        for filename in self._files:
            with fileinput.FileInput(filename, inplace=True, backup=backup) as file:
                for line in file:
                    line_new = re.sub(self._initial_version, str(self._version), line, flags=re.M)
                    if line_new != line:
                        changed_lines.append(f"@Line::{file.lineno()} -> {filename}")
                        print(line_new, end='')
                    else:
                        print(line, end='')
        log.debug(f'Versioner changed {len(changed_lines)} lines')
        return changed_lines if len(changed_lines) > 0 else None

    def _assert_extension(self) -> bool:
        """ Assert that an extension is part of the version """
        if not self._version.state:
            self._version.state = VersionState.DEVELOPMENT
            self._initial_version = f'{self._initial_version}(-(DEVELOPMENT|SNAPSHOT|STABLE|RELEASE))?'

            return False
        return True

    def _assert_exist(self, files: List[str]) -> List[str]:
        """ Assert all file paths exist """
        check_argument(files and all(list(map(os.path.exists, files))),
                       "All files must exist in and be writable: {}", self._search_dir, files)
        return files
