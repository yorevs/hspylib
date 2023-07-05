#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.addons.setman
      @file: settings.py
   @created: Thu, 04 Jul 2023
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.addons.setman.setman_config import SetmanConfig
from clitt.addons.setman.setman_enums import SettingsType
from clitt.addons.setman.settings_entry import SettingsEntry
from clitt.addons.setman.settings_service import SettingsService
from datasource.identity import Identity
from hspylib.core.exception.exceptions import ApplicationError
from hspylib.core.tools.commons import file_is_not_empty, safe_delete_file, syserr, sysout, touch_file
from hspylib.modules.security.security import decode_file, encode_file
from typing import Any, Set

import binascii
import contextlib
import logging as log
import os
import uuid


class Settings:
    def __init__(self, configs: SetmanConfig) -> None:
        self._is_open = False
        self._configs = configs
        self._service = SettingsService(self.configs)
        if not file_is_not_empty(self.configs.database):
            self._create()

    @property
    def configs(self) -> SetmanConfig:
        return self._configs

    @contextlib.contextmanager
    def open(self) -> None:
        """Decode and open the SQL lite database file. Return the context to manipulate it."""
        try:
            if not self._is_open:
                self._is_open = True
                self._decode()
                log.debug("Settings database open")
            yield self._is_open
        except (UnicodeDecodeError, binascii.Error) as err:
            log.error("Failed to open settings file => %s", err)
            yield None
        except Exception as err:
            raise ApplicationError(f"Unable to open settings file => {self.configs.database}", err) from err
        finally:
            self.close()

    def close(self) -> None:
        """Encode and open the SQL lite database file. Return the context to manipulate it."""
        try:
            if self._is_open:
                self._is_open = False
                self._encode()
                log.debug("Settings database closed")
        except (UnicodeDecodeError, binascii.Error) as err:
            log.error("Failed to close settings file => %s", err)
        except Exception as err:
            raise ApplicationError(f"Unable to close settings file => {self.configs.database}", err) from err
        finally:
            safe_delete_file(self.configs.encoded_db)
            safe_delete_file(self.configs.decoded_db)

    def list(self) -> Set[SettingsEntry]:
        """List all database settings using as a formatted table."""
        return set(map(lambda e: e.values, self._service.list()))

    def search(self, name: str, stype: SettingsType, simple_fmt: bool) -> Set[str]:
        """Display all settings matching the name and settings type."""
        return set(map(lambda e: e.to_string(simple_fmt), self._service.search(name, stype)))

    def remove(self, name: str) -> None:
        """Delete the specified setting."""
        if name:
            found = self._service.get(name)
            if found:
                self._service.remove(found)
                sysout("%GREEN%Settings deleted: %ORANGE%", found.name)
            else:
                syserr("Settings not found: ", name)

    def get(self, name: str, simple_fmt: bool) -> None:
        """Get the specified setting."""
        if name:
            found = self._service.get(name)
            if found:
                sysout(found.to_string(simple_fmt))
            else:
                syserr("Settings not found: ", name)

    def upsert(self, name: str, value: Any, stype: SettingsType) -> None:
        """Upsert the specified setting."""
        found = self._service.get(name)
        entry = found or SettingsEntry(Identity(SettingsEntry.SetmanId(uuid.uuid4().hex)), name, value, stype)
        if not name or not value or not stype:
            entry = SettingsEntry.prompt(entry)
        if entry:
            self._service.save(entry)
            sysout(f"%GREEN%Settings {'added' if not found else 'saved'}: %BLUE%", repr(entry))

    def clear(self) -> None:
        """Clear all settings from the settings table."""
        self._service.clear()

    def _create(self) -> bool:
        """Create the settings SQLite DB file."""
        touch_file(self.configs.database)
        self._service.create_db()
        log.info("Settings file has been created")
        self._is_open = True
        return os.path.exists(self.configs.database)

    def _encode(self) -> None:
        """Decode the Base64 encoded database file."""
        if file_is_not_empty(self.configs.database):
            encoded = f"{self.configs.database}-encoded"
            encode_file(self.configs.database, encoded, binary=True)
            os.rename(encoded, self.configs.database)
            self._is_open = False
            log.debug("Settings file is encoded")

    def _decode(self) -> None:
        """Base64 encode the database file."""
        if file_is_not_empty(self.configs.database):
            decoded = f"{self.configs.database}-decoded"
            decode_file(self.configs.database, decoded, binary=True)
            os.rename(decoded, self.configs.database)
            self._is_open = True
            log.debug("Settings file is decoded")
