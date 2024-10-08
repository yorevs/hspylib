#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Hqt
   @package: demo.qtdemos.calculator
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from calculator.views.main_qt_view import MainQtView
from hqt.qt_application import QtApplication
from hspylib.core.tools.commons import parent_path
from hspylib.modules.application.version import Version

import sys

HERE = str(parent_path(__file__))


class Main(QtApplication):
    """QT Calculator main class"""

    def __init__(self, app_name: str):
        version = Version.load(load_dir=HERE)
        super().__init__(MainQtView, app_name, version, resource_dir=f"{HERE}/resources")


if __name__ == "__main__":
    # Application entry point
    Main("Qt_Calculator").INSTANCE.run(sys.argv[1:])
