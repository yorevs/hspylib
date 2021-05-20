#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.firebase.src.main.core
      @file: firebase.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import os
from typing import List
from firebase.src.main.core.agent_config import AgentConfig
from firebase.src.main.core.file_processor import FileProcessor
from hspylib.core.tools.commons import file_is_not_empty



class Firebase:
    """Represents the firebase agent and it's functionalities"""
    
    def __init__(self):
        self.payload = None
        self.processor = FileProcessor()
        self.configs = AgentConfig()
    
    def __str__(self):
        return str(self.payload)
    
    def setup(self) -> None:
        """Setup a firebase creating or reading an existing configuration file"""
        if file_is_not_empty(self.configs.config_file()):
            self.configs.load()
        else:
            self.configs.prompt()
        log.debug(self.configs)
    
    def upload(self, db_alias: str, file_paths: List[str]) -> bool:
        """Upload file_paths to firebase"""
        url = self.configs.url(db_alias)
        assert len(file_paths) > 0, "Unable to upload file_paths (zero size)."
        return self.processor.upload_files(url, file_paths) > 0
    
    def download(self, db_alias: str, dest_dir: str) -> bool:
        """Download file_paths from firebase"""
        url = self.configs.url(db_alias)
        return self.processor.download_files(url, dest_dir or os.environ.get('HOME')) > 0
    
    def is_configured(self) -> bool:
        return self.configs is not None and self.configs.fb_configs is not None
