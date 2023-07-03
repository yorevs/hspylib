#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.setman
      @file: setman_service.py
   @created: Mon, 5 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.addons.setman.setman_config import SetmanConfig
from clitt.addons.setman.setman_entry import SetmanEntry
from clitt.addons.setman.setman_enums import SettingsType
from clitt.addons.setman.setman_repository import SetmanRepository
from datasource.crud_service import CrudService
from textwrap import dedent
from typing import List, Optional


class SetmanService(CrudService[SetmanRepository, SetmanEntry]):
    """Provides a CRUD service for the Setman application."""

    def __init__(self, setman_config: SetmanConfig):
        super().__init__(SetmanRepository(setman_config))

    def get(self, name: str) -> Optional[SetmanEntry]:
        """Get a setman entry using the specified name.
        :param name: the setman entry name to find.
        """
        return self.repository.find_by_name(name)

    def search(self, name: str, stype: SettingsType = None) -> List[SetmanEntry]:
        """Get a setman entry using the specified name.
        :param name: the setman entry name to find.
        :param stype: the settings type to filter.
        """
        return self.repository.search(name, stype)

    def truncate_settings_db(self) -> None:
        """Truncate the settings table."""
        self.repository.truncate("SETTINGS")

    def create_settings_db(self) -> None:
        """Create a brand new setman database file."""
        self.repository.execute(
            dedent(
                """
        CREATE TABLE IF NOT EXISTS "SETTINGS"
        (
            uuid         TEXT       not null,
            name         TEXT       not null,
            value        TEXT       not null,
            stype        TEXT       not null,
            modified     TEXT       not null,

            CONSTRAINT UUID_pk PRIMARY KEY (uuid),
            CONSTRAINT NAME_uk UNIQUE (name)
        )
        """
            )
        )
