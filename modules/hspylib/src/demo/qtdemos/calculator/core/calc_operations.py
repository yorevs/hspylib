#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.calculator.enum
      @file: calc_operations.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.core.enums.enumeration import Enumeration


class CalcOperations(Enumeration):
    NO_OP = None
    DIVISION = "/"
    MULTIPLICATION = "x"
    SUBTRACTION = "-"
    SUM = "+"
    PERCENT = "%"
