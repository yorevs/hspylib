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
from clitt.core.tui.table.table_enums import TextAlignment
from clitt.core.tui.table.table_renderer import TableRenderer
from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import InvalidArgumentError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_state
from hspylib.core.tools.commons import file_is_not_empty, syserr, sysout
from hspylib.modules.application.application import Application
from hspylib.modules.cli.keyboard import Keyboard
from setman.core.setman_config import SetmanConfig
from setman.core.setman_enums import SetmanOps, SettingsType
from setman.settings.settings import Settings
from typing import Any

import atexit
import logging as log
import os


class Setman(metaclass=Singleton):
    """HsPyLib application that helps managing system settings."""

    RESOURCE_DIR = os.environ.get("HHS_DIR", os.environ.get("HOME", "~/"))

    SETMAN_CONFIG_FILE = "setman.properties"

    SETMAN_DB_FILE = f"{RESOURCE_DIR}/.setman-db"

    def __init__(self, parent_app: Application) -> None:
        self._parent_app = parent_app
        cfg_file = f"{self.RESOURCE_DIR}/{self.SETMAN_CONFIG_FILE}"
        if not file_is_not_empty(cfg_file):
            self._setup(cfg_file)
        self._configs = SetmanConfig(self.RESOURCE_DIR, self.SETMAN_CONFIG_FILE)
        self._settings = Settings(self.configs)

    def __str__(self):
        data = set(self.settings.search())
        vault_str = ""
        for entry in data:
            vault_str += entry.key
        return vault_str

    def __repr__(self):
        return str(self)

    @property
    def configs(self) -> SetmanConfig:
        return self._configs

    @property
    def settings(self) -> Settings:
        return self._settings

    def execute(
        self,
        operation: SetmanOps,
        name: str | None,
        value: Any | None,
        stype: SettingsType = None,
        simple_fmt: bool = False,
        filepath: str = None,
    ) -> None:
        """Execute the specified operation."""
        log.debug("%s Name: %s Value: %s SettingsType: %s", operation, name or "*", "-", stype or "*")
        atexit.register(self.settings.close)
        with self.settings.open():
            match operation:
                case SetmanOps.LIST:
                    self._list_settings(name, stype)
                case SetmanOps.SEARCH:
                    self._search_settings(name or "*", stype, simple_fmt)
                case SetmanOps.SET:
                    self._set_setting(name, value, stype)
                case SetmanOps.GET:
                    self._get_setting(name, simple_fmt)
                case SetmanOps.DEL:
                    self._del_setting(name)
                case SetmanOps.TRUNCATE:
                    self._clear_settings(name, stype)
                case SetmanOps.IMPORT:
                    self._import_settings(filepath)
                case SetmanOps.EXPORT:
                    self._export_settings(filepath, name, stype)
                case _:
                    raise InvalidArgumentError(f"Operation not supported: {operation}")

    def _set_setting(self, name: str | None, value: Any | None, stype: SettingsType | None) -> None:
        """Upsert the specified setting.
        :param name: the settings name.
        :param value: the settings value.
        :param stype: the settings type.
        """
        found, entry = self.settings.upsert(name, value, stype)
        sysout(f"%GREEN%Settings {'added' if not found else 'saved'}: %WHITE%", entry, "%EOL%")

    def _get_setting(self, name: str, simple_fmt: bool = False) -> None:
        """Get setting matching the specified name.
        :param name: the settings name to get.
        :param simple_fmt: whether to format the setting or not.
        """
        if found := self.settings.get(name):
            sysout(found.to_string(simple_fmt))
        else:
            syserr("%EOL%%YELLOW%No settings found matching: %WHITE%", name, "%EOL%")

    def _del_setting(self, name: str) -> None:
        """Delete specified setting.
        :param name: the settings name to delete.
        """
        if found := self.settings.remove(name):
            sysout("%GREEN%Setting deleted: %WHITE%", found, "%EOL%")
        else:
            syserr("%EOL%%YELLOW%No settings found matching: %WHITE%", name, "%EOL%")

    def _list_settings(self, name: str | None, stype: SettingsType | None) -> None:
        """List in a table all settings matching criteria.
        :param name: the settings name to filter.
        :param stype: the settings type to filter.
        """
        data = list(map(lambda s: s.values, self.settings.search(name, stype)))
        tr = TableRenderer(self.settings.HEADERS, data, "Systems Settings")
        tr.adjust_auto_fit()
        tr.set_header_alignment(TextAlignment.CENTER)
        tr.set_cell_alignment(TextAlignment.LEFT)
        tr.render()

    def _search_settings(self, name: str | None, stype: SettingsType | None, simple_fmt: bool) -> None:
        """Search and display all settings matching criteria.
        :param name: the settings name to filter.
        :param stype: the settings type to filter.
        :param simple_fmt: whether to display simple or formatted.
        """
        data = list(map(lambda e: e.to_string(simple_fmt), self.settings.search(name, stype)))
        sysout(
            os.linesep.join(data) if data else "%EOL%%YELLOW%No settings found matching: %WHITE%",
            f"[name={name or '*'}, stype={stype or '*'}]",
            "%EOL%",
        )

    def _clear_settings(self, name: str | None, stype: SettingsType | None) -> None:
        """Clear all settings.
        :param name: clear settings matching name.
        """
        if not name and not stype:
            sysout("%EOL%%ORANGE%All settings will be removed. Are you sure (y/[n])? ")
            if (keystroke := Keyboard.wait_keystroke()) and keystroke in [Keyboard.VK_y, Keyboard.VK_Y]:
                self.settings.clear("*", stype)
                sysout("%EOL%%ORANGE%!!! All settings have been removed !!!%EOL%")
        else:
            self.settings.clear(name, stype)
            sysout(
                "%EOL%%ORANGE%Removed settings matching: %WHITE%",
                f"[name={name or '*'}, stype={stype or '*'}]",
                "%EOL%",
            )

    def _import_settings(self, filepath: str) -> None:
        """Import settings from CSV file."""
        count = self.settings.import_csv(filepath)
        sysout(f"%EOL%%GREEN%Imported {count} settings from {filepath}! %EOL%")

    def _export_settings(self, filepath: str, name: str | None = None, stype: SettingsType | None = None) -> None:
        """Import settings from CSV file."""
        count = self.settings.export_csv(filepath, name, stype)
        sysout(f"%EOL%%GREEN%Exported {count} settings to {filepath}! %EOL%")

    def _setup(self, filepath: str) -> None:
        """Setup SetMan on the system."""
        with open(filepath, "w+", encoding=Charset.UTF_8.val) as f_configs:
            f_configs.write(f"hhs.setman.database = {self.SETMAN_DB_FILE} {os.linesep}")
            f_configs.write("hhs.setman.encode.database = True")
            check_state(os.path.exists(filepath), "Unable to create Setman configuration file: " + filepath)
