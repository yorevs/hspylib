#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.versioner.entity
      @file: version.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import re

from enums.extension import Extension
from hspylib.core.tools.constants import RE_VERSION_STRING
from hspylib.core.tools.preconditions import check_argument


class Version:

    @classmethod
    def parse(cls, version_str: str) -> 'Version':
        check_argument(bool(re.match(RE_VERSION_STRING, version_str)),
                       "Version string {} does not match the expected syntax: {}", version_str, RE_VERSION_STRING)
        parts = list(map(str.strip, re.split(r'[.-]', version_str)))
        return Version(
            int(parts[0]),
            int(parts[1]),
            int(parts[2]),
            Extension.value_of(parts[3]) if len(parts) > 3 else None)

    @classmethod
    def of(cls, version: tuple) -> 'Version':
        check_argument(len(version) >= 3, 'Version must contains at least 3 parts: (major, minor, build)')
        return Version(
            int(version[0]),
            int(version[1]),
            int(version[2]),
            Extension.value_of(version[3]) if len(version) > 3 else None)

    def __init__(
        self,
        major: int,
        minor: int,
        patch: int,
        state: Extension):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.state = state

    def __str__(self):
        release = '-' + str(self.state) if self.state else ''
        return f"{self.major:d}.{self.minor:d}.{self.patch:d}{release:s}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return \
            self.major == other.major \
            and self.minor == other.minor \
            and self.patch == other.patch \
            and self.state == other.state

    def __len__(self):
        return 4 if self.state else 3
