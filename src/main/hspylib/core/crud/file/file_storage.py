#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.main.hspylib.core.crud.file
      @file: file_storage.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import ast
import logging as log
import os


class FileStorage:
    """TODO"""

    def __init__(self, filename: str):
        self.filename = filename
        self.data = []
        self.load()
        log.debug(f"File storage filename={self.filename} created and loaded entries={len(self.data)}")

    def load(self) -> None:
        """TODO"""
        mode = 'r+' if os.path.exists(self.filename) else 'w+'
        with open(self.filename, mode) as f_local_db:
            lines = f_local_db.read()
            if lines:
                saved_data = ast.literal_eval(lines)
                self.data = saved_data
        log.debug(f"File storage filename={self.filename} loaded {len(self.data)} entries")

    def commit(self) -> None:
        """TODO"""
        with open(self.filename, 'w') as f_local_db:
            f_local_db.write(str(self.data))
        log.debug(f"File storage filename={self.filename} committed entries={len(self.data)}")

    def truncate(self) -> None:
        """TODO"""
        open(self.filename, 'w').close()
        log.warning(f"File storage filename={self.filename} was truncated")
