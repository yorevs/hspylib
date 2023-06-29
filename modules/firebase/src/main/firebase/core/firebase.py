#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Firebase
   @package: firebase.core
      @file: firebase.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from firebase.core.agent_config import AgentConfig
from firebase.core.file_processor import FileProcessor
from firebase.core.firebase_auth import FirebaseAuth
from hspylib.core.preconditions import check_argument
from typing import List

import logging as log
import os


class Firebase:
    """Provides the firebase application functionalities."""

    def __init__(self) -> None:
        self.processor = FileProcessor()
        filename = os.environ.get(
            "HHS_FIREBASE_CONFIG_FILE", f"{os.environ.get('HOME', os.curdir)}/firebase.properties"
        )
        self.agent_config = AgentConfig(filename)

    def __str__(self):
        return str(self.agent_config)

    def setup(self) -> None:
        """Setup a firebase configuration by creating or reading an existing configuration file."""
        status = False
        while status is not None and not status:
            status = self.agent_config.prompt()
        log.debug("New firebase setup: %s", self.agent_config)

    def upload(self, db_alias: str, file_paths: List[str], glob_exp: str) -> bool:
        """Upload files to firebase.
        :param db_alias: the firebase database alias.
        :param file_paths: the file paths to be uploaded. File paths will be filtered by glob expressions.
        :param glob_exp: the GLOB expressions to filter the input files/folders.
        """
        self._authenticate()
        url = f"{self.agent_config.url(db_alias)}.json"
        check_argument(len(file_paths) > 0, "Unable to upload file_paths (zero size).")
        log.debug("Uploading files  alias=%s  files=[%s]", db_alias, ",".join(file_paths))
        return self.processor.upload_files(url, file_paths, glob_exp) > 0

    def download(self, db_alias: str, dest_dir: str) -> bool:
        """Download specified aliased files from firebase.
        :param db_alias: the database alias to download from.
        :param dest_dir: the destination directory.
        """
        self._authenticate()
        url = f"{self.agent_config.url(db_alias)}.json"
        log.debug("Downloading files  alias=%s  dest_dir=%s", db_alias, dest_dir)
        return self.processor.download_files(url, dest_dir or os.environ.get("HOME")) > 0

    def is_configured(self) -> bool:
        """Checks whether firebase is properly configured or not."""
        return self.agent_config is not None and self.agent_config.firebase_configs is not None

    def _authenticate(self) -> None:
        """Authenticate to Firebase using the user UID."""
        configs = self.agent_config.firebase_configs
        FirebaseAuth.authenticate(configs.project_id, configs.uid)
