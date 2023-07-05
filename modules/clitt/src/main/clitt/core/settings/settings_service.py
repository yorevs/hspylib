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

from clitt.addons.setman.setman_enums import SettingsType
from clitt.core.settings.settings_config import SettingsConfig
from clitt.core.settings.settings_entry import SettingsEntry
from clitt.core.settings.settings_repository import SettingsRepository


class SettingsService(CrudService[SettingsRepository, SettingsEntry]):
    """Provides a CRUD service for the Setman application."""

    def __init__(self, setman_config: SettingsConfig):
        super().__init__(SettingsRepository(setman_config))

    def get(self, name: str) -> Optional[SettingsEntry]:
        """Get settings entry using the specified name.
        :param name: the settings name to get.
        """
        return self.repository.find_by_name(name)

    def search(
        self,
        name: str,
        stype: SettingsType = None,
        limit: int = 500,
        offset: int = 0) -> List[SettingsEntry]:
        """Search settings matching the specified name.
        :param name: the settings name to search.
        :param stype: the settings type to filter.
        :param limit: the max amount of records to search.
        :param offset: the records offset from which to search.
        """
        return self.repository.search(name, stype, limit, offset)

    def clear(self, name: str = None) -> None:
        """Clear all settings from the settings table matching the specified name.
        :param name: the settings name to search.
        """
        self.repository.clear(name)

    def create_db(self) -> None:
        """Create a brand new setman database file."""
        self.repository.create_db()
