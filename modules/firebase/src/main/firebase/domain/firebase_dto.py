#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Firebase
   @package: firebase.domain
      @file: firebase_dto.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from hspylib.core.enums.charset import Charset
from hspylib.core.zoned_datetime import now
from hspylib.modules.security.security import b64_decode, b64_encode
from typing import List

import json
import logging as log
import os


class FirebaseDto:
    """Represents a Firebase DTO."""

    @staticmethod
    def from_file(filepath: str, contents: str | bytes, encoding: str = Charset.UTF_8.val) -> "FirebaseDto":
        """Create a new file entry with the specified contents and expected size.
        :param filepath: the file path.
        :param contents: the file content.
        :param encoding: the file encoding type.
        """
        entry = FirebaseDto(
            filepath, len(contents), str(contents, encoding=encoding) if isinstance(contents, bytes) else contents
        )

        return entry

    @staticmethod
    def from_json(json_string: str) -> List["FirebaseDto"]:
        """Convert a JSON formatted string into a Firebase DTO.
        :param json_string: the JSON string to be converted.
        """
        json_obj = json.loads(json_string)
        return list(map(lambda o: FirebaseDto(o["path"], o["size"], o["data"], o["modified"]), json_obj))

    def __init__(self, file_path: str, size: int = 0, data: str = None, modified: str = None):
        self.path = file_path
        self.size = size
        self.data = data
        self.modified = modified or now()

    def __str__(self) -> str:
        return str({"path": self.path, "data": str(self.data), "size": self.size, "modified": self.modified})

    def load(self) -> "FirebaseDto":
        """Loads the file contents."""
        if os.path.exists(self.path):
            with open(self.path, "r", encoding=Charset.UTF_8.val) as f_in:
                self.data = f_in.read()
                if (size := len(self.data)) == 0:
                    log.warning('Nothing to be loaded. File "%s" is empty', self.path)
                self.size = size
                return self
        raise FileNotFoundError(f'File "{self.path}" could not be loaded because it does not exist!')

    def save(self) -> "FirebaseDto":
        """Saves current DTO content (overwrites current file content)."""
        if os.path.exists(self.path):
            log.warning('File "%s" exists and will be overwritten', self.path)
        with open(self.path, "w+", encoding=Charset.UTF_8.val) as f_out:
            f_out.write(self.data)
            f_out.flush()
            return self

    def encode(self) -> "FirebaseDto":
        """B64-Encode the entry contents."""
        self.data = b64_encode(self.data)
        return self

    def decode(self) -> "FirebaseDto":
        """B64-Decode the entry contents."""
        self.data = b64_decode(self.data)
        return self
