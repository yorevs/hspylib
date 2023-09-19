#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.setman
      @file: setman_entry.py
   @created: Mon, 5 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from collections import namedtuple
from textwrap import dedent
from typing import Any, Optional, Union

from datasource.crud_entity import CrudEntity
from datasource.identity import Identity
from hspylib.core.tools.text_tools import environ_name
from hspylib.core.zoned_datetime import now

from clitt.addons.setman.setman_enums import SettingsType
from clitt.core.tui.minput.menu_input import MenuInput
from clitt.core.tui.minput.minput import minput


class SetmanEntry(CrudEntity):
    """Represents the Setman domain object."""

    SetmanId = namedtuple("SetmanId", ["uuid"])

    # Setman entry display format.
    _DISPLAY_FORMAT = dedent(
        """
    [%BLUE%{}%NC%]:
            Type: %GREEN%{}%NC%
           Value: %GREEN%{}%NC%
        Modified: %GREEN%{}%NC%
    """
    )

    # Setman entry simple format.
    _SIMPLE_FORMAT = "{}={}"

    @staticmethod
    def prompt(entry: Union["SetmanEntry", None] = None) -> Optional["SetmanEntry"]:
        """Create a vault entry from a form input."""

        entry = entry or SetmanEntry()
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label('Name') \
                .min_max_length(1, 60) \
                .value(entry.name) \
                .build() \
            .field() \
                .label('Value') \
                .min_max_length(1, 60) \
                .value(entry.value) \
                .build() \
            .field() \
                .label('Type') \
                .itype('select') \
                .dest('stype') \
                .value(SettingsType.selectables(entry.stype) if entry.stype else None) \
                .build() \
            .build()
        # fmt: on

        if result := minput(form_fields, "Please fill the settings details"):
            entry.name = result.name
            entry.value = result.value
            entry.stype = result.stype
            entry.modified = now()

        return entry if result else None

    def __init__(
        self,
        entity_id: Identity = SetmanId(Identity.auto().values),
        name: str = None,
        value: Any | None = None,
        stype: SettingsType = None,
        modified: str = now(),
    ):
        super().__init__(entity_id)
        self.name = name
        self.value = value
        self.stype = stype.val if stype else SettingsType.PROPERTY.val
        self.modified = modified

    def __str__(self) -> str:
        return str(self.as_dict())

    def __repr__(self) -> str:
        return str(self)

    def to_string(self, simple: bool = False) -> str:
        """Return the string representation of this entry.
        """
        if simple:
            return self._SIMPLE_FORMAT.format(environ_name(self.name), self.value) \
                if self.stype == SettingsType.ENVIRONMENT.val \
                else self._SIMPLE_FORMAT.format(self.name, self.value)
        else:
            return self._DISPLAY_FORMAT.format(self.name, self.stype, self.value, self.modified)
