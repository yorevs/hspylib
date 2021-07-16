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

   Copyright 2021, HSPyLib team
"""
from abc import ABC

from PyQt5.QtGui import QColor

MAX_HISTORY_SIZE_BYTES = 250

# pylint: disable=too-few-public-methods
class StatusColor(ABC):
    """TODO"""
    white = QColor('#FFFFFF')
    red = QColor('#FF0000')
    green = QColor('#00FF00')
    yellow = QColor('#FFFF00')
    blue = QColor('#2380FA')
    orange = QColor('#FF8C36')
