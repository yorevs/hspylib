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
from clitt.addons.setman.setman_config import SetmanConfig
from clitt.addons.setman.setman_enums import SetmanOps, SettingsType
from clitt.addons.setman.settings import Settings
from clitt.core.tui.table.table_enums import TextAlignment
from clitt.core.tui.table.table_renderer import TableRenderer
from hspylib.core.enums.charset import Charset
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import file_is_not_empty, sysout
from hspylib.modules.application.application import Application
from hspylib.modules.cli.keyboard import Keyboard
from typing import Any

import atexit
import logging as log
import os


class SetMan(metaclass=Singleton):
    RESOURCE_DIR = os.environ.get("HHS_DIR", os.environ.get("HOME", "~/"))

    SETMAN_CONFIG_FILE = f"setman.properties"

    SETMAN_DB_FILE = f"{RESOURCE_DIR}/.setman-db"

    def __init__(self, parent_app: Application) -> None:
        self._parent_app = parent_app
        cfg_file = f"{self.RESOURCE_DIR}/{self.SETMAN_CONFIG_FILE}"
        if not file_is_not_empty(cfg_file):
            self._setup(cfg_file)
        self._configs = SetmanConfig(self.RESOURCE_DIR, self.SETMAN_CONFIG_FILE)
        self._settings = Settings(self.configs)

    def __str__(self):
        data = set(self.settings.list())
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
    ) -> None:
        """Execute the specified operation."""
        log.debug(f"{operation} Name: {name or '*'} Value: {value or '-'} SettingsType: {stype or '*'}")
        atexit.register(self.settings.close)
        with self.settings.open():
            match operation:
                case SetmanOps.LIST:
                    self._list_settings()
                case SetmanOps.SEARCH:
                    self._search_settings(name or "%", stype, simple_fmt)
                case SetmanOps.SET:
                    self.settings.upsert(name, value, stype)
                case SetmanOps.GET:
                    self.settings.get(name, simple_fmt)
                case SetmanOps.DEL:
                    self.settings.remove(name)
                case SetmanOps.TRUNCATE:
                    if self._clear_settings():
                        sysout("%EOL%%ORANGE%!!! All system settings have been removed !!!%EOL%")

    def _list_settings(self) -> None:
        """Display all settings."""
        data = self.settings.list()
        headers = ["uuid", "name", "value", "settings type", "modified"]
        tr = TableRenderer(headers, data, "Systems Settings")
        tr.adjust_auto_fit()
        tr.set_header_alignment(TextAlignment.CENTER)
        tr.set_cell_alignment(TextAlignment.LEFT)
        tr.render()

    def _search_settings(self, name: str, stype: SettingsType, simple_fmt: bool) -> None:
        """Search all settings matching criteria."""
        data = self.settings.search(name, stype, simple_fmt)
        sysout(os.linesep.join(data)) if data else sysout(f"%YELLOW%%EOL%No settings found matching '{name}'")

    def _clear_settings(self) -> bool:
        """Clear all settings."""
        sysout("%ORANGE%All settings will be removed. Are you sure (y/[n])? %NC%")
        keystroke = Keyboard.wait_keystroke()
        if keystroke and keystroke in [Keyboard.VK_y, Keyboard.VK_Y]:
            self.settings.clear()
            return True
        return False

    def _setup(self, filepath: str) -> bool:
        """Setup SetMan on the system."""
        with open(filepath, "w+", encoding=Charset.UTF_8.val) as f_configs:
            f_configs.write(f"hhs.setman.database = {self.SETMAN_DB_FILE} {os.linesep}")
        return os.path.exists(filepath)
