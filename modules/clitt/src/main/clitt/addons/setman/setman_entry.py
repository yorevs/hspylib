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
from hspylib.core.zoned_datetime import now

from clitt.core.tui.minput.menu_input import MenuInput
from clitt.core.tui.minput.minput import minput


class SetmanEntry(CrudEntity):
    """Represents the SetMan domain object."""

    SetmanId = namedtuple("SetmanId", ["uuid"])

    # SetMan entry format to be displayed when listing
    _DISPLAY_FORMAT = dedent(
        """
    [%BLUE%{}%NC%]:
            Name: %GREEN%{}%NC%
           Value: %GREEN%{}%NC%
        Modified: %GREEN%{}%NC%
    """
    )

    @staticmethod
    def prompt(existing_entry: Union["SetmanEntry", None] = None) -> Optional["SetmanEntry"]:
        """Create a vault entry from a form input."""

        entry = existing_entry or SetmanEntry()
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label('Name') \
                .min_max_length(3, 50) \
                .value(entry.name) \
                .build() \
            .field() \
                .label('Value') \
                .min_max_length(3, 50) \
                .value(entry.value) \
                .build() \
            .build()
        # fmt: on

        if result := minput(form_fields, "Please fill the settings details"):
            entry.key = result.name
            entry.name = result.name
            entry.modified = now()

        return entry if result else None

    def __init__(
        self,
        entity_id: Identity = SetmanId(Identity.auto().values),
        name: str = None,
        value: Any | None = None,
        modified: str = now(),
    ):
        self.id = None  # Will be filled later
        super().__init__(entity_id)
        self.name = name
        self.value = value
        self.modified = modified

    def __str__(self) -> str:
        return str(self.as_dict())

    def __repr__(self) -> str:
        return str(self)

    def to_string(self) -> str:
        """Return the string representation of this entry.
        """
        return self._DISPLAY_FORMAT.format(self.id, self.name, self.value, self.modified)
