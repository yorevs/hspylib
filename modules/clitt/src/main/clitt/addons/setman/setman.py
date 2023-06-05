#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.addons.setman
      @file: setman.py
   @created: Fri, 29 May 2023
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
import contextlib
import os
from typing import Any

from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import ApplicationError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import file_is_not_empty, safe_delete_file, syserr, touch_file
from hspylib.modules.application.application import Application
from hspylib.modules.security.security import decode_file, encode_file

from clitt.addons.setman.setman_config import SetmanConfig
from clitt.addons.setman.setman_service import SetmanService

import logging as log


class SetMan(metaclass=Singleton):

    RESOURCE_DIR = os.environ.get('HHS_DIR', os.environ.get('HOME', '~/'))

    SETMAN_CONFIG_FILE = 'setman.properties'

    DEFAULT_CONFIGS = [
        'hhs.setman.user = %USERNAME%',
        'hhs.setman.passphrase = %PASSWORD%',
        'hhs.setman.database = %DATABASE%',
    ]

    def __init__(self, parent_app: Application) -> None:
        self._parent_app = parent_app
        cfg_file = f"{self.RESOURCE_DIR}/{self.SETMAN_CONFIG_FILE}"
        if not file_is_not_empty(cfg_file):
            self._setup(cfg_file)
        self._configs = SetmanConfig(self.RESOURCE_DIR, self.SETMAN_CONFIG_FILE)
        self._service = SetmanService(self._configs)
        self._is_open = False
        if not file_is_not_empty(self._configs.database):
            self._create_new_database()

    def __str__(self):
        data = set(self._service.list())
        vault_str = ""
        for entry in data:
            vault_str += entry.key
        return vault_str

    @property
    def configs(self) -> SetmanConfig:
        return self._configs

    def execute(self, operation: str, name: str, value: Any | None) -> None:
        """Execute the specified operation."""
        pass

    @contextlib.contextmanager
    def _open_db(self) -> bool:
        """Decode and open the SQL lite database file. Return the context to manipulate it."""
        try:
            if not self._is_open:
                self._decode_db()
                log.debug("Settings database open")
            yield self._is_open or None
        except UnicodeDecodeError as err:
            log.error("Failed to open settings file => %s", err)
            syserr("Failed to open settings file")
            yield None
        finally:
            self._close_db()

        return self._is_open

    def _close_db(self) -> bool:
        """Encode and open the SQL lite database file. Return the context to manipulate it."""
        try:
            if self._is_open:
                self._encode_db()
                log.debug("Settings database closed")
        except UnicodeDecodeError as err:
            log.error("Failed to close settings file => %s", err)
            syserr("Failed to close settings file")
            return False
        except Exception as err:
            raise ApplicationError(f"Unable to close settings file => {self._configs.database}", err) from err

        return True

    def _encode_db(self) -> None:
        encoded = f"{self._configs.database}-encoded"
        encode_file(self._configs.database, encoded, binary=True)
        safe_delete_file(encoded)
        log.debug("Settings file is encoded")

    def _decode_db(self) -> None:
        encoded = f"{self._configs.database}-encoded"
        decode_file(self._configs.database, encoded, binary=True)
        safe_delete_file(encoded)
        log.debug("Settings file is decoded")

    def _create_new_database(self) -> bool:
        """Create the settings SQLite DB file."""
        touch_file(self._configs.database)
        self._service.create_settings_db()
        log.info('Settings file has been created')
        return os.path.exists(self._configs.database)

    def _setup(self, filepath: str) -> bool:
        """Setup SetMan on the system."""
        with open(filepath, "w+", encoding=Charset.UTF_8.val) as f_configs:
            lines = list(map(lambda c: c + os.linesep, self.DEFAULT_CONFIGS))
            f_configs.writelines(lines)
        return os.path.exists(filepath)
