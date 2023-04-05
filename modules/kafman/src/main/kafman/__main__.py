#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Kafman
   @package: kafman
      @file: __main__.py
   @created: Fri, 1 Jul 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import logging as log
import sys
from textwrap import dedent

from hspylib.core.enums.charset import Charset
from hspylib.core.zoned_datetime import now
from hspylib.modules.application.version import Version
from hspylib.modules.qt.qt_application import QtApplication

from kafman.__classpath__ import _Classpath
from kafman.views.main_qt_view import MainQtView


class Main(QtApplication):
    """Kafman application main class"""

    # The welcome message
    DESCRIPTION = _Classpath.get_source_path("welcome.txt").read_text(encoding=Charset.UTF_8.val)

    # Location of the .version file
    VERSION_DIR = _Classpath.source_path()

    # Location of the resources dir
    RESOURCE_DIR = str(_Classpath.resource_path())

    # Location of the UI font
    FONT_PATH = _Classpath.get_resource_path("fonts/Droid-Sans-Mono-for-Powerline-Nerd-Font-Complete.otf")

    # Application icon
    APP_ICON_PATH = _Classpath.get_resource_path("app-icon.png")

    def __init__(self, app_name: str):
        version = Version.load(load_dir=self.VERSION_DIR)
        description = self.DESCRIPTION.format(version)
        super().__init__(MainQtView, app_name, version, description, resource_dir=self.RESOURCE_DIR)
        self.set_application_font(self.FONT_PATH)
        self.set_application_icon(self.APP_ICON_PATH)
        log.info(
            dedent(
                f"""
        {self._app_name} v{self._app_version}

        Settings ==============================
                STARTED: {now("%Y-%m-%d %H:%M:%S")}
        """
            )
        )


if __name__ == "__main__":
    # Application entry point
    Main("kafman").INSTANCE.run(sys.argv[1:])
