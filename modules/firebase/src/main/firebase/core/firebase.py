#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.firebase.core
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

from hspylib.core.tools.preconditions import check_argument

from firebase.core.agent_config import AgentConfig
from firebase.core.file_processor import FileProcessor


class Firebase:
    """Represents the firebase agent and it's functionalities"""

    def __init__(self):
        self.processor = FileProcessor()
        self.agent_config = AgentConfig()

    def __str__(self):
        return str(self.agent_config)

    def setup(self) -> None:
        """Setup a firebase creating or reading an existing firebase configuration file"""
        self.agent_config.prompt()
        log.debug(self.agent_config)

    def upload(self, db_alias: str, file_paths: List[str], glob_exp: str) -> bool:
        """Upload files to firebase"""
        url = self.agent_config.url(db_alias)
        check_argument(len(file_paths) > 0, "Unable to upload file_paths (zero size).")
        return self.processor.upload_files(url, file_paths, glob_exp) > 0

    def download(self, db_alias: str, dest_dir: str) -> bool:
        """Download files from firebase specified by it's aliases"""
        url = self.agent_config.url(db_alias)
        return self.processor.download_files(url, dest_dir or os.environ.get('HOME')) > 0

    def is_configured(self) -> bool:
        """Checks whether firebase is properly configured or not"""
        return self.agent_config is not None and self.agent_config.firebase_configs is not None
