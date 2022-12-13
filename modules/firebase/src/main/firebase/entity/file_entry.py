#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.firebase.entity
      @file: file_entry.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.enums.charset import Charset
from hspylib.core.preconditions import check_state

import base64
import logging as log
import os


class FileEntry:
    """TODO"""

    @staticmethod
    def of(file_path: str, file_data: bytes, expected_size: int) -> "FileEntry":
        """Create a new file entry with the specified contents and expected size"""
        file_entry = FileEntry(file_path)
        file_entry.data = file_data
        file_entry.decode()
        file_entry.size = len(file_entry.data)
        check_state(
            file_entry.size == expected_size,
            f"Received data and expected data sizes mismatch: {file_entry.size} vs {expected_size}",
        )

        return file_entry

    def __init__(self, file_path: str):
        self.path = file_path
        self.size = 0
        self.data = None
        self.load()

    def __str__(self) -> str:
        return '{"path" : "' + self.path + '", "size" : ' + str(self.size) + ', "data" : "' + self.data + '"}'

    def load(self) -> "FileEntry":
        """TODO"""
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f_in:
                self.data = f_in.read()
                self.size = len(self.data)
                log.warning('File "%s" is empty', self.path)

        return self

    def save(self) -> "FileEntry":
        """Write current file data into this file"""
        with open(self.path, "w+", encoding="utf-8") as f_in:
            f_in.write(self.data)
            f_in.flush()

        return self

    def encode(self) -> "FileEntry":
        """B64 Encode this file's data"""
        self.data = str(base64.urlsafe_b64encode(self.data.encode(Charset.UTF_8.val)), encoding=Charset.UTF_8.val)
        return self

    def decode(self) -> "FileEntry":
        """B64 Decode this file's data"""
        self.data = str(base64.urlsafe_b64decode(self.data), encoding=Charset.UTF_8.val)
        return self
