#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.crud.file
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
    def __init__(self, filename: str):
        self.filename = filename
        self.data = []
        self.load()
        log.debug('File storage filename={} created and loaded entries={}'.format(filename, len(self.data)))
    
    def load(self) -> None:
        mode = 'r+' if os.path.exists(self.filename) else 'w+'
        with open(self.filename, mode) as f_local_db:
            lines = f_local_db.read()
            if lines:
                saved_data = ast.literal_eval(lines)
                self.data = saved_data
    
    def commit(self) -> None:
        with open(self.filename, 'w') as f_local_db:
            f_local_db.write(str(self.data))
        log.debug('File storage filename={} committed entries={}'.format(self.filename, len(self.data)))
    
    def truncate(self) -> None:
        open(self.filename, 'w').close()
        log.warning('File storage filename={} was truncated'.format(self.filename))
