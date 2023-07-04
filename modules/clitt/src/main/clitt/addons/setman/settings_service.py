#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.setman
      @file: settings_service.py
   @created: Mon, 5 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from typing import List, Optional

from datasource.crud_service import CrudService
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.keyboard import Keyboard

from clitt.addons.setman.setman_config import SetmanConfig
from clitt.addons.setman.setman_enums import SettingsType
from clitt.addons.setman.settings_entry import SettingsEntry
from clitt.addons.setman.settings_repository import SettingsRepository


class SettingsService(CrudService[SettingsRepository, SettingsEntry]):
    """Provides a CRUD service for the Setman application."""

    def __init__(self, setman_config: SetmanConfig):
        super().__init__(SettingsRepository(setman_config))

    def get(self, name: str) -> Optional[SettingsEntry]:
        """Get a setman entry using the specified name.
        :param name: the setman entry name to find.
        """
        return self.repository.find_by_name(name)

    def search(self, name: str, stype: SettingsType = None) -> List[SettingsEntry]:
        """Get a setman entry using the specified name.
        :param name: the setman entry name to find.
        :param stype: the settings type to filter.
        """
        return self.repository.search(name, stype)

    def truncate_settings_db(self) -> bool:
        """Truncate the settings table."""
        sysout("All settings will be removed. Are you sure (y/[n])? ")
        keystroke = Keyboard.wait_keystroke()
        if keystroke and keystroke in [Keyboard.VK_y, Keyboard.VK_Y]:
            self.repository.truncate()
            return True
        return False

    def create_settings_db(self) -> None:
        """Create a brand new setman database file."""
        self.repository.create_db()
