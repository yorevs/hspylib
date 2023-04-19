#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   main.addons.appman.templates
      @file: widget.py.tpl
   @created: Tue, 1 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.addons.widman.widget import Widget
from clitt.core.icons.font_awesome.widget_icons import WidgetIcons
from concurrent import futures
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cli.keyboard import Keyboard
from time import sleep
from typing import List


class Widget_WIDGET_NAME_(Widget):
  """HsPyLib to do something"""
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
    sysout("I am: ", str(self))
    sysout("And I'm running ...")
    sysout('Done.')
