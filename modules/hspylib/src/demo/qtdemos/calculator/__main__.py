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
from hspylib.core.tools.commons import get_path
from hspylib.modules.application.version import Version
from hspylib.modules.qt.qt_application import QtApplication
from qtdemos.calculator.views.main_qt_view import MainQtView

import sys

HERE = str(get_path(__file__))


class Main(QtApplication):
    """QT Calculator main class"""

    def __init__(self, app_name: str):
        version = Version.load(load_dir=HERE)
        super().__init__(MainQtView, app_name, version, resource_dir=f"{HERE}/resources")


if __name__ == "__main__":
    # Application entry point
    Main("Qt_Calculator").INSTANCE.run(sys.argv[1:])
