#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.cli.vt100
      @file: vt100_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from time import sleep

from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.vt100.vt_utils import alternate_screen

if __name__ == "__main__":
    alternate_screen()
    sysout("%CSV%Cursor saved")
    sleep(1)
    sysout("%MOD(1;31)%RED%MOD(0)%")
    sysout("%MOD(1;32)%GREEN%MOD(0)%")
    sleep(1)
    sysout("%CUU(2)%", end="")
    sleep(1)
    sysout("%MOD(1;36)%MA%MOD(0)%")
    sleep(2)
    sysout("%USC%HIDDEN_TEXT")
    sysout("%SSC%VISIBLE_TEXT")
    sleep(2)
    sysout("%CUP(3;2)%ELLO THERE(3;1)", end="")
    sleep(2)
    sysout("%CUP(4;3)%EW HERE(4;3)", end="")
    sleep(2)
    sysout("%CRE%%EL0%", end="")
    sysout("Done")
    sysout("%ED0%", end="")
    alternate_screen(False)
