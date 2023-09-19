#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.qt
      @file: qt_application.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import sys
from pathlib import Path
from typing import TypeVar

from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import QApplication

from hspylib.core.preconditions import check_argument, check_state
from hspylib.core.tools.text_tools import titlecase
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import Version

V = TypeVar('V', bound='QWidget')


class QtApplication(Application):

    def __init__(
        self,
        main_view: V,
        name: str,
        version: Version,
        description: str = None,
        usage: str = None,
        epilog: str = None,
        resource_dir: str = None,
        log_dir: str = None):
        super().__init__(name, version, description, usage, epilog, resource_dir, log_dir)
        app_title = titlecase(name)
        self.qapp = QApplication(sys.argv)
        self.main_view = main_view()
        self.main_view.window.setWindowTitle(f"{app_title} v{str(version)}")
        self.qapp.setApplicationDisplayName(app_title)
        self.qapp.setApplicationName(name)
        self.qapp.setApplicationVersion(str(version))
        self.qapp.setQuitOnLastWindowClosed(True)

    def _main(self, *params, **kwargs) -> int:
        """Execute the application's main statements"""
        self.main_view.show()
        return self.qapp.exec_()

    def _cleanup(self) -> None:
        QApplication.exit()

    def set_application_font(self, font_path: Path) -> None:
        """TODO"""
        check_argument(font_path.exists(), f'Could not find font at: {str(font_path)}')
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        families = QFontDatabase.applicationFontFamilies(font_id)
        check_state(families is not None and len(families) == 1)
        self.qapp.setFont(QFont(families[0], 14))

    def set_application_icon(self, icon_path: Path) -> None:
        """TODO"""
        check_argument(icon_path.exists(), f'Could not find icon file at: {str(icon_path)}')
        self.qapp.setWindowIcon(QIcon(str(icon_path)))
