#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: __main__.py
   @created: Thu, 21 Jul 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import sys
from hspylib.core.tools.commons import get_path
from hspylib.modules.cli.application.version import Version
from hspylib.modules.qt.qt_application import QtApplication
from qtdemos.promotions.views.main_qt_view import MainQtView

HERE = str(get_path(__file__))


class Main(QtApplication):
    """QT HPromotions main class"""

    def __init__(self, app_name: str):
        version = Version.load(load_dir=HERE)
        super().__init__(MainQtView, app_name, version, resource_dir=f'{HERE}/resources')


if __name__ == "__main__":
    # Application entry point
    Main('Qt_HS_Promotions').INSTANCE.run(sys.argv[1:])
