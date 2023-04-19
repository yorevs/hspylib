#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: demo.qtdemos.calculator.views
      @file: blink_lcd_thread.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from threading import Thread
from time import sleep

from hspylib.core.config.app_config import AppConfigs
from PyQt5.QtWidgets import QLCDNumber


class BlinkLcdThread(Thread):
    def __init__(self, lcd: QLCDNumber):
        Thread.__init__(self)
        self._lcd = lcd
        self._configs = AppConfigs.INSTANCE

    def run(self):
        palette = self._lcd.palette()
        fg_color = palette.color(palette.WindowText)
        bg_color = palette.color(palette.Background)
        palette.setColor(palette.WindowText, bg_color)
        self._lcd.setPalette(palette)
        sleep(float(self._configs["lcd.blink.delay"]))
        palette.setColor(palette.WindowText, fg_color)
        self._lcd.setPalette(palette)
