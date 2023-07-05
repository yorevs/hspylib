#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.cli.settings
      @file: settings_demo.py
   @created: Wed, 5 Jul 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from hspylib.core.tools.commons import sysout

from clitt.addons.setman.setman_enums import SettingsType
from clitt.core.settings.settings import Settings
from clitt.core.settings.settings_config import SettingsConfig

if __name__ == "__main__":
    configs = SettingsConfig("resources", "settings-demo.properties")
    settings = Settings(configs)
    with settings.open() as s:
        s.upsert("demo.settings.one", True, SettingsType.PROPERTY)
        s.upsert("demo.settings.two", False, SettingsType.ENVIRONMENT)
        s["demo.settings.three"] = "VALUE", SettingsType.PROPERTY
        sysout(s)
        sysout(s["demo.settings.one"].to_string())
