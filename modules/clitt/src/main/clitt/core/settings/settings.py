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
import binascii
import contextlib
import logging as log
import os
import uuid
from typing import Any, List, Optional, Tuple

from datasource.identity import Identity
from hspylib.core.exception.exceptions import ApplicationError
from hspylib.core.preconditions import check_state
from hspylib.core.tools.commons import file_is_not_empty, safe_delete_file, touch_file
from hspylib.core.zoned_datetime import now
from hspylib.modules.security.security import decode_file, encode_file

from clitt.addons.setman.setman_enums import SettingsType
from clitt.core.settings.settings_config import SettingsConfig
from clitt.core.settings.settings_entry import SettingsEntry
from clitt.core.settings.settings_service import SettingsService


class Settings:
    """Class to provide settings interactions."""

    def __init__(self, configs: SettingsConfig) -> None:
        self._is_open = False
        self._configs = configs
        self._service = SettingsService(self.configs)
        if not file_is_not_empty(self.configs.database):
            self._create_db()

    def __str__(self):
        entries = f",{os.linesep}  ".join(list(map(lambda s: str(s), self.list())))
        return (
            f"Settings: [{os.linesep + '  ' if entries else ''}"
            f"{entries}"
            f"{os.linesep if entries else ''}]"
        )

    def __repr__(self):
        return str(self)

    def __getitem__(self, name: str) -> SettingsEntry:
        return self.get(name)

    def __setitem__(self, name: str, item: Tuple[Any, SettingsType]) -> None:
        self.upsert(name, item[0], item[1])

    @property
    def configs(self) -> SettingsConfig:
        return self._configs

    @property
    def is_open(self) -> bool:
        return self._is_open

    @is_open.setter
    def is_open(self, new_is_open: bool) -> None:
        self._is_open = new_is_open
        log.debug(f"Settings database open: {self.configs.database}")

    @contextlib.contextmanager
    def open(self) -> None:
        """Decode and open the SQL lite database file. Return the context to manipulate it."""
        try:
            if not self.is_open:
                if self.configs.is_db_encoded:
                    self._decode_db_file()
                self.is_open = True
            yield self
        except (UnicodeDecodeError, binascii.Error) as err:
            err_msg = f"Failed to open settings file => {self.configs.database}"
            raise ApplicationError(err_msg, err) from err
        except Exception as err:
            err_msg = f"Unable to close settings file => {self.configs.database}"
            raise ApplicationError(err_msg, err) from err
        finally:
            self.close()

    def close(self) -> None:
        """Encode and open the SQL lite database file. Return the context to manipulate it."""
        try:
            if self._is_open:
                if self.configs.is_db_encoded:
                    self._encode_db_file()
                self._is_open = False
                log.debug(f"Settings database closed: {self.configs.database}")
        except (UnicodeDecodeError, binascii.Error) as err:
            err_msg = f"Failed to close settings file => {self.configs.database}"
            raise ApplicationError(err_msg, err) from err
        except Exception as err:
            err_msg = f"Unable to close settings file => {self.configs.database}"
            raise ApplicationError(err_msg, err) from err
        finally:
            safe_delete_file(self.configs.encoded_db)
            safe_delete_file(self.configs.decoded_db)

    def list(self) -> List[SettingsEntry]:
        """List all database settings using as a formatted table."""
        check_state(self.is_open, "Settings database is not open")
        return self._service.list()

    def search(self, name: str, stype: SettingsType, simple_fmt: bool) -> List[str]:
        """Display all settings matching the name and settings type."""
        check_state(self.is_open, "Settings database is not open")
        return list(map(lambda e: e.to_string(simple_fmt), self._service.search(name, stype)))

    def remove(self, name: str) -> Optional[SettingsEntry]:
        """Delete the specified setting."""
        check_state(self.is_open, "Settings database is not open")
        if name:
            found = self._service.get(name)
            if found:
                self._service.remove(found)
                return found
        return None

    def get(self, name: str) -> Optional[SettingsEntry]:
        """Get the specified setting."""
        check_state(self.is_open, "Settings database is not open")
        if name:
            return self._service.get(name)
        return None

    def upsert(
        self,
        name: str,
        value: Any,
        stype: SettingsType) -> Tuple[Optional[SettingsEntry], Optional[SettingsEntry]]:
        """Upsert the specified setting."""

        check_state(self.is_open, "Settings database is not open")
        found = self._service.get(name)
        entry = found or SettingsEntry(Identity(SettingsEntry.SetmanId(uuid.uuid4().hex)), name, value, stype)
        if not name or value is None or not stype:
            entry = SettingsEntry.prompt(entry)
        if entry:
            entry.modified = now()
            self._service.save(entry)
        return found, entry

    def clear(self) -> None:
        """Clear all settings from the settings table."""
        check_state(self.is_open, "Settings database is not open")
        self._service.clear()

    def _create_db(self) -> bool:
        """Create the settings SQLite DB file."""
        touch_file(self.configs.database)
        self._service.create_db()
        log.info("Settings file has been created")
        self._is_open = True
        return os.path.exists(self.configs.database)

    def _encode_db_file(self) -> None:
        """Decode the Base64 encoded database file."""
        if file_is_not_empty(self.configs.database):
            encoded = f"{self.configs.database}-encoded"
            encode_file(self.configs.database, encoded, binary=True)
            os.rename(encoded, self.configs.database)
            log.debug("Settings file is encoded")

    def _decode_db_file(self) -> None:
        """Base64 encode the database file."""
        if file_is_not_empty(self.configs.database):
            decoded = f"{self.configs.database}-decoded"
            decode_file(self.configs.database, decoded, binary=True)
            os.rename(decoded, self.configs.database)
            log.debug("Settings file is decoded")
