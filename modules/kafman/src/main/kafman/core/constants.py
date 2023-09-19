#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: constants.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from abc import ABC

from PyQt5.QtGui import QColor

MAX_HISTORY_SIZE_BYTES = 250


# pylint: disable=too-few-public-methods
class StatusColor(ABC):
    """Colors to be used in the status text"""
    white = QColor('#FFFFFF')
    red = QColor('#FF554D')
    green = QColor('#28C941')
    yellow = QColor('#FEBE2F')
    blue = QColor('#2380FA')
    orange = QColor('#FF8C36')
    purple = QColor('#D9A2FF')
