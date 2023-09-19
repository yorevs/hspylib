#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.firebase.entity
      @file: file_entry.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import base64
import os

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.preconditions import check_state


class FileEntry:
    """TODO"""

    @staticmethod
    def of(file_path: str, file_data: bytes, expected_size: int) -> 'FileEntry':
        """Create a new file entry with the specified contents and expected size"""
        file_entry = FileEntry(file_path)
        file_entry.data = file_data
        file_entry.decode()
        file_entry.size = len(file_entry.data)
        check_state(file_entry.size == expected_size,
                    "Retrieved data and expected data length mismatch: {} vs {}", expected_size, len(file_entry.data))
        return file_entry

    def __init__(self, file_path: str):
        self.path = file_path
        self.size = 0
        self.data = None
        if os.path.exists(file_path):
            self.size = os.path.getsize(file_path)
            with open(file_path, 'r', encoding='utf-8') as f_in:
                self.data = f_in.read()
                check_state(len(self.data) > 0, "File \"{}\" is empty", file_path)

    def __str__(self) -> str:
        return '{"path" : "' + self.path + '", "size" : ' + str(self.size) + ', "data" : "' + self.data + '"}'

    def encode(self) -> 'FileEntry':
        """B64 Encode this file's data"""
        self.data = base64.urlsafe_b64encode(self.data.encode(str(Charset.UTF_8))).decode(str(Charset.UTF_8))
        return self

    def decode(self) -> 'FileEntry':
        """B64 Decode this file's data"""
        self.data = str(base64.urlsafe_b64decode(self.data), str(Charset.UTF_8))
        return self

    def save(self) -> 'FileEntry':
        """Write current file data into this file"""
        with open(self.path, 'w', encoding='utf-8') as f_in:
            f_in.write(self.data)
        return self
