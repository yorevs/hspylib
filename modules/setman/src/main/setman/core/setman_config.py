#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.setman
      @file: setman_config.py
   @created: Mon, 5 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from setman.settings.settings_config import SettingsConfig


class SetmanConfig(SettingsConfig):
    """Holds the SetMan configurations."""

    def __init__(self, resource_dir: str, filename: str):
        super().__init__(resource_dir, filename)
        self._database: str = self["hhs.setman.database"]
