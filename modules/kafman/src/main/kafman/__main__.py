#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys

from hspylib.core.enums.charset import Charset
from hspylib.modules.cli.application.version import AppVersion
from hspylib.modules.qt.qt_application import QtApplication

from kafman.__classpath__ import _Classpath
from kafman.views.main_qt_view import MainQtView


class Main(QtApplication):
    """Kafman application main class"""

    # The welcome message
    DESCRIPTION = _Classpath.get_source("welcome.txt").read_text(encoding=Charset.UTF_8.value)

    # Location of the .version file
    VERSION_DIR = _Classpath.source_root()

    # Location of the resources dir
    RESOURCE_DIR = _Classpath.resource_dir()

    # Location of the UI font
    FONT_PATH = _Classpath.get_resource('fonts/Droid-Sans-Mono-for-Powerline-Nerd-Font-Complete.otf')

    # Application icon
    APP_ICON_PATH = _Classpath.get_resource('app-icon.png')

    def __init__(self, app_name: str):
        version = AppVersion.load(load_dir=self.VERSION_DIR)
        description = self.DESCRIPTION.format(version)
        super().__init__(MainQtView, app_name, version, description, resource_dir=self.RESOURCE_DIR)
        self.set_application_font(self.FONT_PATH)
        self.set_application_icon(self.APP_ICON_PATH)


if __name__ == "__main__":
    # Application entry point
    Main('kafman').INSTANCE.run(sys.argv[1:])
