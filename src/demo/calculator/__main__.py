#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.demo.calculator
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import os
import sys

from calculator.ui.qt.views.main_qt_view import MainQtView
from hspylib.core.tools.commons import dirname, read_version
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.vt100.vt_utils import exit_app
from hspylib.modules.qt.qt_application import QtApplication


class Main(Application):
    """TODO"""

    # The application name
    APP_NAME = os.path.basename(__file__)

    # Version tuple: (major,minor,build)
    VERSION = (0, 9, 0)

    # Application usage message
    USAGE = f"""
    Usage: {APP_NAME} <option> [arguments]"""

    def __init__(self, app_name: str):
        super().__init__(app_name, read_version(), self.USAGE, dirname(__file__))
        self.main_view = QtApplication(MainQtView)

    def _main(self, *args, **kwargs) -> None:  # pylint: disable=unused-argument
        exit_app(self.main_view.run())


if __name__ == "__main__":
    # Application entry point
    Main('HSPyLib Qt Calculator Demo').INSTANCE.run(sys.argv[1:])
