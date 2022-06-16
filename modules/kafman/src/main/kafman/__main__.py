#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.main.hspylib.addons.appman.templates
      @file: tpl-main.py
   @created: Tue, 1 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import sys

from PyQt5.QtGui import QFontDatabase, QFont
from hspylib.core.tools.preconditions import check_state
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import AppVersion
from hspylib.modules.cli.vt100.vt_utils import exit_app
from hspylib.modules.qt.qt_application import QtApplication

from kafman.__classpath__ import Classpath, get_source, get_resource
from kafman.views.main_qt_view import MainQtView


class Main(Application):
    """Kafman application main class"""

    # The welcome message
    DESCRIPTION = get_source("welcome.txt").read_text()

    # Location of the .version file
    VERSION_DIR = Classpath.SOURCE_ROOT

    # Location of the UI font
    FONT_PATH = str(get_resource('fonts/Droid-Sans-Mono-for-Powerline-Nerd-Font-Complete.otf'))

    def __init__(self, app_name: str):
        version = AppVersion.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version))
        self.qt_app = QtApplication(MainQtView)
        font_id = QFontDatabase.addApplicationFont(self.FONT_PATH)
        families = QFontDatabase.applicationFontFamilies(font_id)
        check_state(families is not None and len(families) == 1)
        font = QFont(families[0], 14)
        self.qt_app.main_view.set_default_font(font)
        self.qt_app.app.setFont(font)

    def _setup_arguments(self) -> None:
        """passInitialize application parameters and options"""

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        exit_app(self.qt_app.run())

    def _cleanup(self) -> None:
        """Execute code cleanup before exiting"""


if __name__ == "__main__":
    # Application entry point
    Main('kafman').INSTANCE.run(sys.argv[1:])
