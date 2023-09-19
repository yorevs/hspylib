#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.enum
      @file: charset.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration


class Charset(Enumeration):
    ASCII = 'ASCII'
    BIG5 = 'BIG5'
    BIG5HKSCS = 'BIG5HKSCS'
    CP037 = 'CP037'
    CP424 = 'CP424'
    CP437 = 'CP437'
    CP500 = 'CP500'
    CP737 = 'CP737'
    CP775 = 'CP775'
    CP850 = 'CP850'
    CP852 = 'CP852'
    CP855 = 'CP855'
    CP856 = 'CP856'
    CP857 = 'CP857'
    CP860 = 'CP860'
    CP861 = 'CP861'
    CP862 = 'CP862'
    CP863 = 'CP863'
    CP864 = 'CP864'
    CP865 = 'CP865'
    CP866 = 'CP866'
    CP869 = 'CP869'
    CP874 = 'CP874'
    CP875 = 'CP875'
    CP932 = 'CP932'
    CP949 = 'CP949'
    CP950 = 'CP950'
    CP1006 = 'CP1006'
    CP1026 = 'CP1026'
    CP1140 = 'CP1140'
    CP1250 = 'CP1250'
    CP1251 = 'CP1251'
    CP1252 = 'CP1252'
    CP1253 = 'CP1253'
    CP1254 = 'CP1254'
    CP1255 = 'CP1255'
    CP1256 = 'CP1256'
    CP1257 = 'CP1257'
    CP1258 = 'CP1258'
    EUC_JP = 'EUC-JP'
    EUC_JIS_2004 = 'EUC-JIS_2004'
    EUC_JISX0213 = 'EUC-JISX0213'
    EUC_KR = 'EUC-KR'
    GB2312 = 'GB2312'
    GBK = 'GBK'
    GB18030 = 'GB18030'
    HZ = 'HZ'
    ISO2022_JP = 'ISO2022-JP'
    ISO2022_JP_1 = 'ISO2022-JP-1'
    ISO2022_JP_2 = 'ISO2022-JP-2'
    ISO2022_JP_2004 = 'ISO2022-JP-2004'
    ISO2022_JP_3 = 'ISO2022-JP-3'
    ISO2022_JP_EXT = 'ISO2022-JP_EXT'
    ISO2022_KR = 'ISO2022-KR'
    LATIN_1 = 'LATIN-1'
    ISO8859_2 = 'ISO8859_2'
    ISO8859_3 = 'ISO8859-3'
    ISO8859_4 = 'ISO8859-4'
    ISO8859_5 = 'ISO8859-5'
    ISO8859_6 = 'ISO8859-6'
    ISO8859_7 = 'ISO8859-7'
    ISO8859_8 = 'ISO8859-8'
    ISO8859_9 = 'ISO8859-9'
    ISO8859_10 = 'ISO8859-10'
    ISO8859_13 = 'ISO8859-13'
    ISO8859_14 = 'ISO8859-14'
    ISO8859_15 = 'ISO8859-15'
    JOHAB = 'JOHAB'
    KOI8_R = 'KOI8-R'
    KOI8_U = 'KOI8-U'
    MAC_CYRILLIC = 'MAC-CYRILLIC'
    MAC_GREEK = 'MAC-GREEK'
    MAC_ICELAND = 'MAC-ICELAND'
    MAC_LATIN2 = 'MAC-LATIN2'
    MAC_ROMAN = 'MAC-ROMAN'
    MAC_TURKISH = 'MAC-TURKISH'
    PTCP154 = 'PTCP154'
    SHIFT_JIS = 'SHIFT-JIS'
    SHIFT_JIS_2004 = 'SHIFT-JIS_2004'
    SHIFT_JISX0213 = 'SHIFT-JISX0213'
    UTF_16 = 'UTF-16'
    UTF_16_BE = 'UTF-16-BE'
    UTF_16_LE = 'UTF-16-LE'
    UTF_7 = 'UTF-7'
    UTF_8 = 'UTF-8'

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)
