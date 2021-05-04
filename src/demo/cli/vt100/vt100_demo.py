#!/usr/bin/env python3
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
