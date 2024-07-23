#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Hqt
   @package: demo.qtdemos.calculator.core
      @file: operations.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from hspylib.core.enums.enumeration import Enumeration


class Operations(Enumeration):
    # fmt: off
    NO_OP           = None
    DIVISION        = '/'
    MULTIPLICATION  = 'x'
    SUBTRACTION     = '-'
    SUM             = '+'
    PERCENT         = '%'
    # fmt: on
