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
from os.path import basename
from typing import Any, Optional

from clitt.core.tui.minput.menu_input import MenuInput
from clitt.core.tui.minput.minput import minput
from clitt.core.tui.table.table_enums import TextAlignment
from clitt.core.tui.table.table_renderer import TableRenderer
from hspylib.core.enums.charset import Charset
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.namespace import Namespace
from hspylib.core.preconditions import check_state
from hspylib.core.tools.commons import dirname, file_is_not_empty, safe_delete_file, syserr, sysout
from hspylib.core.tools.text_tools import ensure_endswith
from hspylib.modules.application.application import Application
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cli.keyboard import Keyboard

from setman.core.setman_config import SetmanConfig
from setman.core.setman_enums import SetmanOps, SettingsType
from setman.settings.settings import Settings


class Setman(metaclass=Singleton):
    """HsPyLib application that helps managing system settings."""

    HHS_SETMAN_CONFIG_FILE = os.environ.get(
        "HHS_SETMAN_CONFIG_FILE", f"{os.environ.get('HOME', os.curdir)}/setman.properties"
    )

    HHS_SETMAN_DB_FILE = os.environ.get("HHS_SETMAN_DB_FILE", f"{os.environ.get('HOME', os.curdir)}/setman.db")

    @staticmethod
    def _prompt(db_file: str) -> Optional[Namespace]:
        """Prompt the user for the settings setup info.
        :param db_file the file that will hold all settings (database file).
        :return: a Namespace containing all filled input.
        """
        # fmt: off
        form_fields = (
            MenuInput.builder()
                .field()
                    .label("Settings File")
                    .dest("db_file")
                    .min_max_length(1, 80)
                    .value(db_file)
                    .build()
            .build()
        )
        return minput(form_fields)

    def __init__(self, parent_app: Application) -> None:
        self._parent_app = parent_app
        cfg_dir, cfg_file = dirname(self.HHS_SETMAN_CONFIG_FILE), basename(self.HHS_SETMAN_CONFIG_FILE)
        if not file_is_not_empty(self.HHS_SETMAN_CONFIG_FILE):
            if not self._setup(self.HHS_SETMAN_CONFIG_FILE):
                self._exec_status = ExitStatus.FAILED
                return
        self._configs = SetmanConfig(cfg_dir, cfg_file)
        self._settings = Settings(self.configs)
        self._exec_status = ExitStatus.SUCCESS

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
        prefix: str | None,
        value: Any | None,
        stype: SettingsType = None,
        simple_fmt: bool = False,
        preserve: bool = False,
        filepath: str | None = None,
    ) -> ExitStatus:
        """Execute the specified operation.
        :param operation the operation to execute against the settings.
        :param name the settings name.
        :param prefix the settings prefix.
        :param value the settings value.
        :param stype the settings type.
        :param simple_fmt whether to format the setting when searching.
        :param preserve whether to preserve (no overwrite) existing settings.
        :param filepath the path of the CSV file to be imported/exported.
        """

        log.debug(
            "<%s> Name: %s  Prefix: %s  Value: %s  SettingsType: %s",
            operation, name or "*", prefix or '<none>', "-", stype or "*")
        self._settings.preserve = preserve

        match operation:
            case SetmanOps.LIST:
                self._list_settings(name, stype)
            case SetmanOps.SEARCH:
                self._search_settings(name or "*", stype, simple_fmt)
            case SetmanOps.SET:
                self._set_setting(name, prefix, value, stype)
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
            case SetmanOps.SOURCE:
                self._source_settings(name, filepath)

        return self._exec_status

    def _set_setting(
        self, name: str | None,
        prefix: str | None,
        value: Any | None,
        stype: SettingsType | None) -> None:
        """Upsert the specified setting.
        :param name the settings name.
        :param value the settings value.
        :param stype the settings type.
        """
        found, entry = self.settings.put(name, prefix, value, stype)
        if entry:
            sysout(f"%GREEN%Settings {'added' if not found else 'saved'}: %WHITE%", entry, "%EOL%")
        else:
            self._exec_status = ExitStatus.FAILED

    def _get_setting(self, name: str, simple_fmt: bool = False) -> None:
        """Get setting matching the specified name.
        :param name the settings name to get.
        :param simple_fmt: whether to format the setting or not.
        """
        if found := self.settings.get(name):
            sysout(found.to_string(simple_fmt))
        else:
            syserr("%EOL%%YELLOW%No settings found matching: %WHITE%", name, "%EOL%")
            self._exec_status = ExitStatus.FAILED

    def _del_setting(self, name: str) -> None:
        """Delete specified setting.
        :param name the settings name to delete.
        """
        if found := self.settings.remove(name):
            sysout("%GREEN%Setting deleted: %WHITE%", found, "%EOL%")
        else:
            syserr("%EOL%%YELLOW%No settings found matching: %WHITE%", name, "%EOL%")
            self._exec_status = ExitStatus.FAILED

    def _list_settings(self, name: str | None, stype: SettingsType | None) -> None:
        """List in a table all settings matching criteria.
        :param name the settings name to filter when listing.
        :param stype the settings type to filter when listing.
        """
        data = list(map(lambda s: s.values[1:], self.settings.search(name, stype)))
        tr = TableRenderer(self.settings.HEADERS[1:], data, "Systems Settings")
        tr.set_header_alignment(TextAlignment.CENTER)
        tr.set_cell_alignment(TextAlignment.LEFT)
        tr.render()

    def _search_settings(self, name: str | None, stype: SettingsType | None, simple_fmt: bool) -> None:
        """Search and display all settings matching criteria.
        :param name the settings name to filter when searching.
        :param stype the settings type to filter when searching.
        :param simple_fmt: whether to display simple or formatted.
        """
        data = list(map(lambda e: e.to_string(simple_fmt), self.settings.search(name, stype)))
        if data:
            if not simple_fmt:
                l_data = len(data)
                diff_offset = self.settings.limit - self.settings.offset
                sysout(
                    "%YELLOW%{} {}%NC%".format(
                        f"\n-=- Listing {'top' if l_data > diff_offset else 'all'} {min(l_data, diff_offset)} "
                        f"system settings matching: ",
                        f"[name={name or '*'}, stype={stype or '*'}] -=-",
                        "%EOL%"
                    )
                )
            sysout(os.linesep.join(data))
        else:
            if not simple_fmt:
                sysout(
                    "%EOL%%YELLOW%No settings found matching: %WHITE%",
                    f"[name={name or '*'}, stype={stype or '*'}]",
                    "%EOL%"
                )
            self._exec_status = ExitStatus.FAILED

    def _clear_settings(self, name: str | None, stype: SettingsType | None) -> None:
        """Clear all settings.
        :param name the settings name to filter when clearing.
        :param stype the settings type to filter when clearing.
        """
        if not name and not stype:
            sysout("%EOL%%YELLOW%All settings will be removed. Are you sure (y/[n])? ")
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
        """Import settings from CSV file.
        :param filepath the path of the importing file.
        """
        count = self.settings.import_csv(filepath)
        sysout(f"%EOL%%GREEN%Imported {count} settings from {filepath}! %EOL%")

    def _export_settings(self, filepath: str, name: str | None = None, stype: SettingsType | None = None) -> None:
        """Import settings from CSV file.
        :param filepath the path of the exporting file.
        :param name the settings name to filter when exporting.
        :param stype the settings type to filter when exporting.
        """
        count = self.settings.export_csv(filepath, name, stype)
        sysout(f"%EOL%%GREEN%Exported {count} settings to {filepath}! %EOL%")

    def _source_settings(self, name: str | None, filepath: str | None) -> None:
        """Source (bash export) all environment settings to current shell.
        :param name the settings name to filter when sourcing.
        """
        prefixed = ensure_endswith((name or "").replace("*", "%"), "%")
        data = os.linesep.join(self.settings.as_environ(prefixed))
        if filepath:
            with open(filepath, "a", encoding=Charset.UTF_8.val) as f_exports:
                f_exports.writelines(data)
        else:
            sysout(data)

    def _setup(self, filepath: str) -> bool:
        """Setup SetMan on the system.
        :param filepath the path of the Setman configuration file.
        """
        with open(filepath, "w+", encoding=Charset.UTF_8.val) as f_configs:
            if result := self._prompt(self.HHS_SETMAN_DB_FILE):
                check_state(os.path.exists(dirname(result.db_file)), f"Unable to find database path: f{result.db_file}")
                f_configs.write(f"hhs.setman.database = {result.db_file} {os.linesep}")
                check_state(os.path.exists(filepath), "Unable to create Setman configuration file: " + filepath)
                return True
            safe_delete_file(filepath)
            return False
