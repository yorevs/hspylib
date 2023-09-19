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

from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import AppVersion
from hspylib.modules.cli.vt100.vt_utils import exit_app
from hspylib.modules.qt.qt_application import QtApplication

from kafman.__classpath__ import Classpath, get_source
from kafman.views.main_qt_view import MainQtView


class Main(Application):
    """Kafman application main class"""

    # The welcome message
    DESCRIPTION = get_source("welcome.txt").read_text()

    # Location of the .version file
    VERSION_DIR = Classpath.SOURCE_ROOT

    def __init__(self, app_name: str):
        version = AppVersion.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version))
        self.main_view = QtApplication(MainQtView)

    def _setup_arguments(self) -> None:
        """passInitialize application parameters and options"""

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        exit_app(self.main_view.run())

    def _cleanup(self) -> None:
        """Execute code cleanup before exiting"""


if __name__ == "__main__":
    # Application entry point
    Main('kafman').INSTANCE.run(sys.argv[1:])
