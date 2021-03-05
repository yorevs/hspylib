#!/usr/bin/env python3
from hspylib.ui.cli.vt100.vt_codes import vt_print

if __name__ == '__main__':
    vt_print('%VT_CSV%')
    vt_print('%VT_MOD(1;35)%HUGO%VT_MOD(0)%\n')
    vt_print('%VT_MOD(1;33)%HUGO%VT_MOD(0)%\n')
    vt_print('%VT_CUU(2)%')
    vt_print('%VT_MOD(1;36)%GE%VT_MOD(0)%\n')
    vt_print('%VT_USC%HIDDEN_TEXT\n')
    vt_print('%VT_SSC%VISIBLE_TEXT\n')
    vt_print('%VT_CRE%')
    vt_print('Done')
