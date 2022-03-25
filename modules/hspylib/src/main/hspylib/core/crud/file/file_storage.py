#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.crud.file
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
        log.debug("File storage filename=%s created and loaded entries=%d", self.filename, len(self.data))

    def load(self) -> None:
        """TODO"""
        mode = 'r+' if os.path.exists(self.filename) else 'w+'
        with open(self.filename, mode, encoding='utf-8') as f_local_db:
            lines = f_local_db.read()
            if lines:
                saved_data = ast.literal_eval(lines)
                self.data = saved_data
        log.debug("File storage filename=%s loaded %d entries", self.filename, len(self.data))

    def commit(self) -> None:
        """TODO"""
        with open(self.filename, 'w', encoding='utf-8') as f_local_db:
            f_local_db.write(str(self.data))
        log.debug("File storage filename=%s committed entries=%d", self.filename, len(self.data))

    def truncate(self) -> None:
        """TODO"""
        with open(self.filename, 'w', encoding='utf-8'):
            log.warning("File storage filename=%s was truncated", self.filename)
