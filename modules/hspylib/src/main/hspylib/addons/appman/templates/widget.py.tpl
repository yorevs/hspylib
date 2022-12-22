#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   main.addons.appman.templates
      @file: widget.py.tpl
   @created: Tue, 1 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from concurrent import futures
from time import sleep
from typing import List

from hspylib.addons.widman.widget import Widget
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons
from hspylib.modules.cli.keyboard import Keyboard


class Widget_WIDGET_NAME_(Widget):
  """HSPyLib to do something"""
  WIDGET_ICON = WidgetIcons.WIDGET
  WIDGET_NAME = "_WIDGET_NAME_"
  TOOLTIP = "TODO Widget tooltip"
  USAGE = "Usage: _WIDGET_NAME_"
  VERSION = (0, 1, 0)

  def __init__(self):
    super().__init__(
      self.WIDGET_ICON,
      self.WIDGET_NAME,
      self.TOOLTIP,
      self.USAGE,
      self.VERSION)
    self._exit_code = ExitStatus.SUCCESS

  def execute(self, args: List[str] = None) -> ExitStatus:
    with futures.ThreadPoolExecutor() as executor:
      done = False
      while not done and not Keyboard.kbhit():
        future = executor.submit(self._do_something)
        done = not future.result()
        sleep(0.5)

    return self._exit_code

  def cleanup(self) -> None:
    # If your widget requires any cleanup procedures
    pass

  def _do_something(self) -> None:
    sysout(str(self))
    sysout('My widget is running')
    sysout('')
