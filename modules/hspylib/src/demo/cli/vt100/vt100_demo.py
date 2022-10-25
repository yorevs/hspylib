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

   Copyright 2022, HSPyLib team
"""
from time import sleep

from hspylib.modules.cli.vt100.vt_codes import vt_print
if __name__ == '__main__':
    vt_print('%CSV%Cursor saved', end='\n')
    sleep(1)
    vt_print('%MOD(1;31)%RED%MOD(0)%', end='\n')
    vt_print('%MOD(1;32)%GREEN%MOD(0)%\n')
    sleep(1)
    vt_print('%CUU(2)%')
    sleep(1)
    vt_print('%MOD(1;36)%MA%MOD(0)%\n')
    sleep(1)
    vt_print('%USC%HIDDEN_TEXT\n')
    vt_print('%SSC%VISIBLE_TEXT\n')
    sleep(1)
    vt_print('%CRE%%EL0%')
    vt_print('Done')
    vt_print('%ED0%')
