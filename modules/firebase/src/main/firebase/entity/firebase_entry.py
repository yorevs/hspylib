#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.firebase.entity
      @file: firebase_entry.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from firebase.entity.file_entry import FileEntry
from hspylib.core.enums.charset import Charset
from hspylib.core.zoned_datetime import now
from typing import List

import json


class FirebaseEntry:
    def __init__(
        self,
        name: str = None,
        last_update_user: str = None,
        files: List[FileEntry] = None,
        encoding: Charset = Charset.UTF_8,
    ):
        self.name = name
        self.last_update_user = last_update_user
        self.files = files if files else []
        self.str_encoding = str(encoding).lower()
        self.last_modified = now("%d/%m/%Y %H:%M:%S")

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return str(self)

    def payload(self) -> str:
        """Return a firebase request payload for this entry"""
        return str(
            {
                "encoding": self.str_encoding,
                "file_paths": str(self.files),
                "last_modified": self.last_modified,
                "last_update_user": self.last_update_user,
            }
        )
