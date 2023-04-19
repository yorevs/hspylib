#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from %APP_NAME%.__classpath__ import _Classpath
from %APP_NAME%.view.main_qt_view import MainQtView
from hqt.qt_application import QtApplication
from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import get_path
from hspylib.modules.application.version import Version

import sys

HERE = get_path(__file__)


class Main(QtApplication):
  """TODO"""

  # The welcome message
  DESCRIPTION = (HERE / "welcome.txt").read_text(encoding=Charset.UTF_8.val)

  # Location of the .version file
  VERSION_DIR = _Classpath.source_path()

  # Location of the resource directory
  RESOURCE_DIR = str(_Classpath.resource_path())

  def __init__(self, app_name: str):
    version = Version.load(load_dir=self.VERSION_DIR)
    description = self.DESCRIPTION.format(version)
    super().__init__(MainQtView, app_name, version, description, resource_dir=self.RESOURCE_DIR)


if __name__ == "__main__":
  # Application entry point
  Main('Application name').INSTANCE.run(sys.argv[1:])
