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
import logging as log
import os
import uuid
from typing import Any

from datasource.identity import Identity
from hspylib.core.enums.charset import Charset
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import file_is_not_empty, syserr, sysout, touch_file
from hspylib.modules.application.application import Application

from clitt.addons.setman.setman_config import SetmanConfig
from clitt.addons.setman.setman_entry import SetmanEntry
from clitt.addons.setman.setman_enums import SetmanOps, SettingsType
from clitt.addons.setman.setman_service import SetmanService
from clitt.core.tui.table.table_renderer import TableRenderer


class SetMan(metaclass=Singleton):

    RESOURCE_DIR = os.environ.get('HHS_DIR', os.environ.get('HOME', '~/'))

    SETMAN_CONFIG_FILE = f"setman.properties"

    SETMAN_DB_FILE = f"{RESOURCE_DIR}/.setman-db"

    def __init__(self, parent_app: Application) -> None:
        self._parent_app = parent_app
        cfg_file = f"{self.RESOURCE_DIR}/{self.SETMAN_CONFIG_FILE}"
        if not file_is_not_empty(cfg_file):
            self._setup_db(cfg_file)
        self._configs = SetmanConfig(self.RESOURCE_DIR, self.SETMAN_CONFIG_FILE)
        self._service = SetmanService(self.configs)
        if not file_is_not_empty(self.configs.database):
            self._create_new_database()

    def __str__(self):
        data = set(self._service.list())
        vault_str = ""
        for entry in data:
            vault_str += entry.key
        return vault_str

    def __repr__(self):
        return str(self)

    @property
    def configs(self) -> SetmanConfig:
        return self._configs

    def execute(
        self,
        operation: SetmanOps,
        name: str | None,
        value: Any | None,
        stype: SettingsType = None,
        simple_fmt: bool = False) -> None:

        """Execute the specified operation."""
        log.debug(f"{operation} Name: {name or '*'} Value: {value or '-'} SettingsType: {stype or '*'}")
        match operation:
            case SetmanOps.LIST:
                self._list_settings()
            case SetmanOps.SEARCH:
                self._search_settings(name or '%', stype, simple_fmt)
            case SetmanOps.SET:
                self._add_setting(name, value, stype)
            case SetmanOps.GET:
                self._get_setting(name, simple_fmt)
            case SetmanOps.DEL:
                self._del_setting(name)
            case SetmanOps.TRUNCATE:
                self._service.truncate_settings_db()
                sysout('All settings have been removed')

    def _list_settings(self) -> None:
        """List all database settings using as a formatted table."""
        headers = ["uuid", "name", "value", "settings type", "modified"]
        data = list(map(lambda e: e.values, self._service.list()))
        tr = TableRenderer(headers, data, "Systems Settings")
        tr.adjust_auto_fit()
        tr.set_header_alignment(TableRenderer.TextAlignment.CENTER)
        tr.set_cell_alignment(TableRenderer.TextAlignment.LEFT)
        tr.render()

    def _search_settings(self, name: str, stype: SettingsType, simple_fmt: bool) -> None:
        """Display all settings matching the name and settings type."""
        data = list(map(lambda e: e.to_string(simple_fmt), self._service.search(name, stype)))
        sysout(os.linesep.join(data))

    def _del_setting(self, name: str) -> None:
        """TODO"""
        if name:
            found = self._service.get(name)
            if found:
                self._service.remove(found)
                sysout('%GREEN%Settings deleted: %ORANGE%', found.name)
            else:
                syserr('Settings not found: ', name)

    def _get_setting(self, name: str, simple_fmt: bool) -> None:
        """TODO"""
        if name:
            found = self._service.get(name)
            if found:
                sysout(found.to_string(simple_fmt))
            else:
                syserr('Settings not found: ', name)

    def _add_setting(self, name: str, value: Any, stype: SettingsType) -> None:
        """TODO"""
        found = self._service.get(name)
        entry = found or SetmanEntry(Identity(SetmanEntry.SetmanId(uuid.uuid4().hex)), name, value, stype)
        if not name or not value or not stype:
            entry = SetmanEntry.prompt(entry)
        if entry:
            self._service.save(entry)
            sysout(f"%GREEN%Settings {'added' if not found else 'saved'}: %BLUE%", repr(entry))

    def _create_new_database(self) -> bool:
        """Create the settings SQLite DB file."""
        touch_file(self.configs.database)
        self._service.create_settings_db()
        log.info('Settings file has been created')
        self._is_open = True
        return os.path.exists(self.configs.database)

    def _setup_db(self, filepath: str) -> bool:
        """Setup SetMan on the system."""
        with open(filepath, "w+", encoding=Charset.UTF_8.val) as f_configs:
            f_configs.write(f"hhs.setman.database = {self.SETMAN_DB_FILE} {os.linesep}")
        return os.path.exists(filepath)
