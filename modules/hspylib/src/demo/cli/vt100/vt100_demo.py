#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.cli.vt100
      @file: vt100_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.modules.cli.vt100.vt_codes import vt_print

if __name__ == '__main__':
    vt_print('%CSV%')
    vt_print('%MOD(1;35)%HUGO%MOD(0)%\n')
    vt_print('%MOD(1;33)%HUGO%MOD(0)%\n')
    vt_print('%CUU(2)%')
    vt_print('%MOD(1;36)%GE%MOD(0)%\n')
    vt_print('%USC%HIDDEN_TEXT\n')
    vt_print('%SSC%VISIBLE_TEXT\n')
    vt_print('%CRE%')
    vt_print('Done')
