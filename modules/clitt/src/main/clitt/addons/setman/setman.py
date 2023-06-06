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
import atexit
import binascii
import contextlib
import logging as log
import os
import uuid
from typing import Any

from datasource.identity import Identity
from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import ApplicationError, InvalidArgumentError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.commons import file_is_not_empty, syserr, sysout, touch_file
from hspylib.modules.application.application import Application
from hspylib.modules.security.security import decode_file, encode_file

from clitt.addons.setman.setman_config import SetmanConfig
from clitt.addons.setman.setman_entry import SetmanEntry
from clitt.addons.setman.setman_enums import SetmanOps, SettingsType
from clitt.addons.setman.setman_service import SetmanService
from clitt.core.tui.table.table_renderer import TableRenderer


class SetMan(metaclass=Singleton):

    RESOURCE_DIR = os.environ.get('HHS_DIR', os.environ.get('HOME', '~/'))

    SETMAN_CONFIG_FILE = f"setman.properties"

    SETMAN_DB_FILE = f"{RESOURCE_DIR}/setman.db"

    DEFAULT_CONFIGS = [
        'hhs.setman.database = ' + SETMAN_DB_FILE,
    ]

    def __init__(self, parent_app: Application) -> None:
        atexit.register(self._close_db)
        self._parent_app = parent_app
        cfg_file = f"{self.RESOURCE_DIR}/{self.SETMAN_CONFIG_FILE}"
        if not file_is_not_empty(cfg_file):
            self._setup(cfg_file)
        self._configs = SetmanConfig(self.RESOURCE_DIR, self.SETMAN_CONFIG_FILE)
        self._service = SetmanService(self.configs)
        self._is_open = False
        if not file_is_not_empty(self.configs.database):
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

    def execute(
        self,
        operation: str,
        name: str | None,
        value: Any | None,
        stype: SettingsType = None) -> None:

        """Execute the specified operation."""
        with self._open_db():
            log.debug(f"{operation.upper()} Name: {name or '*'} Value: {value or '-'} SettingsType: {stype or '*'}")
            match SetmanOps.of_value(operation, ignore_case=True):
                case SetmanOps.LIST:
                    self._list_settings()
                case SetmanOps.SEARCH:
                    self._search_settings(name, stype)
                case SetmanOps.SET:
                    self._add_setting(name, stype, value)
                case SetmanOps.GET:
                    check_not_none(name)
                    self._get_setting(name)
                case SetmanOps.DEL:
                    check_not_none(name)
                    self._del_setting(name)
                case SetmanOps.TRUNCATE:
                    self._service.truncate_settings_db()
                    sysout('All settings have been removed')
                case _:
                    raise InvalidArgumentError('Operation not recognized: ' + operation)

    def _list_settings(self):
        headers = ["uuid", "name", "value", "settings type", "modified"]
        data = list(map(lambda e: e.values, self._service.list()))
        tr = TableRenderer(headers, data, "Systems Settings")
        tr.adjust_auto_fit()
        tr.set_header_alignment(TableRenderer.TextAlignment.CENTER)
        tr.set_cell_alignment(TableRenderer.TextAlignment.LEFT)
        tr.render()

    def _search_settings(self, name: str, stype: SettingsType):
        data = list(map(lambda e: e.to_string(), self._service.search(name, stype)))
        sysout(os.linesep.join(data))

    def _del_setting(self, name: str):
        found = self._service.get(name)
        if found:
            self._service.remove(found)
            sysout('Settings deleted:', repr(found))
        else:
            syserr('Settings not found:', name)

    def _get_setting(self, name: str):
        found = self._service.get(name)
        if found:
            sysout('Settings retrieved:', repr(found))
        else:
            syserr('Settings not found:', name)

    def _add_setting(self, name: str, stype: SettingsType, value: Any):
        found = self._service.get(name)
        entry = found or SetmanEntry(Identity(SetmanEntry.SetmanId(uuid.uuid4().hex)), name, value, stype)
        if not entry.name or not entry.value or not entry.stype:
            entry = SetmanEntry.prompt(entry)
        if entry:
            self._service.save(entry)
            sysout(f"Settings {'added' if not found else 'saved'}:", entry)

    @contextlib.contextmanager
    def _open_db(self) -> bool:
        """Decode and open the SQL lite database file. Return the context to manipulate it."""
        try:
            if not self._is_open:
                self._decode_db()
                log.debug("Settings database open")
            yield self._is_open or None
        except (UnicodeDecodeError, binascii.Error) as err:
            log.error("Failed to open settings file => %s", err)
            syserr("Failed to open settings file")
            yield None
        except Exception as err:
            raise ApplicationError(f"Unable to open settings file => {self.configs.database}", err) from err
        finally:
            self._is_open = True
            self._close_db()

        return self._is_open

    def _close_db(self) -> bool:
        """Encode and open the SQL lite database file. Return the context to manipulate it."""
        try:
            if self._is_open:
                self._encode_db()
                log.debug("Settings database closed")
        except (UnicodeDecodeError, binascii.Error) as err:
            log.error("Failed to close settings file => %s", err)
            syserr("Failed to close settings file")
            return False
        except Exception as err:
            raise ApplicationError(f"Unable to close settings file => {self.configs.database}", err) from err

        return True

    def _encode_db(self) -> None:
        """Decode the Base64 encoded database file."""
        if file_is_not_empty(self.configs.database):
            encoded = f"{self.configs.database}-encoded"
            encode_file(self.configs.database, encoded, binary=True)
            os.rename(encoded, self.configs.database)
            self._is_open = False
            log.debug("Settings file is encoded")

    def _decode_db(self) -> None:
        """Base64 encode the database file."""
        if file_is_not_empty(self.configs.database):
            decoded = f"{self.configs.database}-decoded"
            decode_file(self.configs.database, decoded, binary=True)
            os.rename(decoded, self.configs.database)
            self._is_open = True
            log.debug("Settings file is decoded")

    def _create_new_database(self) -> bool:
        """Create the settings SQLite DB file."""
        touch_file(self.configs.database)
        self._service.create_settings_db()
        log.info('Settings file has been created')
        self._is_open = True
        return os.path.exists(self.configs.database)

    def _setup(self, filepath: str) -> bool:
        """Setup SetMan on the system."""
        with open(filepath, "w+", encoding=Charset.UTF_8.val) as f_configs:
            lines = list(map(
                lambda c: c + os.linesep, self.DEFAULT_CONFIGS
            ))
            f_configs.writelines(lines)
        return os.path.exists(filepath)
