#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.setman
      @file: settings_entry.py
   @created: Mon, 5 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from clitt.core.tui.minput.input_validator import InputValidator
from clitt.core.tui.minput.menu_input import MenuInput
from clitt.core.tui.minput.minput import minput
from collections import namedtuple
from datasource.crud_entity import CrudEntity
from datasource.identity import Identity
from hspylib.core.tools.text_tools import ensure_endswith, environ_name, xstr
from hspylib.core.zoned_datetime import now
from setman.core.setman_enums import SettingsType
from textwrap import dedent
from typing import Any, Optional, Union

import re


class SettingsEntry(CrudEntity):
    """Represents the Settings domain entity."""

    SetmanId = namedtuple("SetmanId", ["uuid"])

    # Setman entry display format.
    _DISPLAY_FORMAT = dedent(
        """
    [%BLUE%{}%NC%]:
            Type: %GREEN%{}%NC%
           Value: %GREEN%{}%NC%
          Prefix: %GREEN%{}%NC%
        Variable: %GREEN%{}%NC%
        Modified: %GREEN%{}%NC%
    """
    )

    # Setman entry simple format.
    _SIMPLE_FORMAT = "{}={}"

    @staticmethod
    def prompt(entry: Union["SettingsEntry", None] = None) -> Optional["SettingsEntry"]:
        """Create a settings entry from a form input.
        :param entry: An optional existing entry to edit.
        :return: A new or updated settings entry.
        """

        entry = entry or SettingsEntry()
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label('Name') \
                .min_max_length(1, 60) \
                .validator(InputValidator.custom(r'[a-zA-Z0-9\_\-\.]')) \
                .value(entry.name) \
                .build() \
            .field() \
                .label('Prefix') \
                .min_max_length(0, 30) \
                .validator(InputValidator.custom(r'[a-zA-Z0-9\_\-\.]')) \
                .value(entry.prefix) \
                .build() \
            .field() \
                .label('Value') \
                .min_max_length(1, 90) \
                .validator(InputValidator.custom(r'[^\"\`]')) \
                .value(xstr(entry.value)) \
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
            entry.prefix = result.prefix
            entry.value = result.value
            entry.stype = result.stype
            entry.modified = now()

        return entry if result else None

    def __init__(
        self,
        entity_id: Identity = SetmanId(Identity.auto().values),
        name: str = None,
        prefix: str = "",
        value: Any | None = None,
        stype: SettingsType = None,
        modified: str = now(),
    ):
        super().__init__(entity_id)
        self.name: str = name or ""
        self.prefix: str = prefix if not prefix.endswith(".") else prefix[:-1]
        self.value: Any = value or ""
        self.stype: str = stype.val if stype else SettingsType.PROPERTY.val
        self.modified: str = modified

    def __str__(self) -> str:
        return str(self.as_dict())

    def __repr__(self) -> str:
        return self.to_string()

    @property
    def environ_name(self) -> str:
        """Return the environment variable representation name of this entry."""
        return environ_name(self._de_prefixed()) if self.stype == SettingsType.ENVIRONMENT.val else self.name

    def to_string(self, simple_fmt: bool = False) -> str:
        """Return the string representation of this entry.
        :param simple_fmt: Whether to format the entry or not.
        :return: The string representation of the entry.
        """
        if simple_fmt:
            return (
                self._SIMPLE_FORMAT.format(self.environ_name, xstr(self.value))
                if self.stype == SettingsType.ENVIRONMENT.val
                else self._SIMPLE_FORMAT.format(self.name, xstr(self.value))
            )
        return self._DISPLAY_FORMAT.format(
            self.name, self.stype, xstr(self.value), self.prefix or "<none>", self.environ_name, self.modified
        )

    def to_env_export(self) -> str:
        """Return the bash 'export' command of this entry.
        :return: The bash export command as a string.
        """
        return f'export {self.environ_name}="{xstr(self.value)}"'

    def _de_prefixed(self) -> str:
        """Return the setting name without the prefix.
        :return: The setting name without its prefix.
        """
        prefix = ensure_endswith(self.prefix, ".") if self.prefix else ""
        de_prefixed = re.sub(rf"^{prefix}", "", self.name) if prefix else self.name
        return de_prefixed
