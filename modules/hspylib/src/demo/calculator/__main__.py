#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import os
import sys

from calculator.ui.qt.views.main_qt_view import MainQtView
from hspylib.modules.cli.application.version import AppVersion
from hspylib.modules.qt.qt_application import QtApplication


class Main(QtApplication):
    """QT Calculator main class"""

    def __init__(self, app_name: str):
        version = AppVersion.load(load_dir=os.getcwd())
        super().__init__(MainQtView, app_name, version)


if __name__ == "__main__":
    # Application entry point
    Main('Qt_Calculator').INSTANCE.run(sys.argv[1:])
