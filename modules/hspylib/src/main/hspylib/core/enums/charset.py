#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.enums
      @file: charset.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration


class Charset(Enumeration):
    """Enumeration to wrap all standard charsets."""

    # fmt: off

    ASCII           = 'ascii'
    BIG5            = 'big5'
    BIG5HKSCS       = 'big5hkscs'

    CP037           = 'cp037'
    CP424           = 'cp424'
    CP437           = 'cp437'
    CP500           = 'cp500'
    CP737           = 'cp737'
    CP775           = 'cp775'
    CP850           = 'cp850'
    CP852           = 'cp852'
    CP855           = 'cp855'
    CP856           = 'cp856'
    CP857           = 'cp857'
    CP860           = 'cp860'
    CP861           = 'cp861'
    CP862           = 'cp862'
    CP863           = 'cp863'
    CP864           = 'cp864'
    CP865           = 'cp865'
    CP866           = 'cp866'
    CP869           = 'cp869'
    CP874           = 'cp874'
    CP875           = 'cp875'
    CP932           = 'cp932'
    CP949           = 'cp949'
    CP950           = 'cp950'
    CP1006          = 'cp1006'
    CP1026          = 'cp1026'
    CP1140          = 'cp1140'
    CP1250          = 'cp1250'
    CP1251          = 'cp1251'
    CP1252          = 'cp1252'
    CP1253          = 'cp1253'
    CP1254          = 'cp1254'
    CP1255          = 'cp1255'
    CP1256          = 'cp1256'
    CP1257          = 'cp1257'
    CP1258          = 'cp1258'

    EUC_JP          = 'euc-jp'
    EUC_JIS_2004    = 'euc-jis_2004'
    EUC_JISX0213    = 'euc-jisx0213'
    EUC_KR          = 'euc-kr'
    GB2312          = 'gb2312'
    GBK             = 'gbk'
    GB18030         = 'gb18030'
    HZ              = 'hz'

    ISO2022_JP      = 'iso-2022-jp'
    ISO2022_JP_1    = 'iso-2022-jp-1'
    ISO2022_JP_2    = 'iso-2022-jp-2'
    ISO2022_JP_2004 = 'iso-2022-jp-2004'
    ISO2022_JP_3    = 'iso-2022-jp-3'
    ISO2022_JP_EXT  = 'iso-2022-jp_ext'
    ISO2022_KR      = 'iso-2022-kr'

    LATIN_1         = 'latin-1'
    ISO8859_1       = 'iso-8859-1'
    ISO8859_2       = 'iso-8859-2'
    ISO8859_3       = 'iso-8859-3'
    ISO8859_4       = 'iso-8859-4'
    ISO8859_5       = 'iso-8859-5'
    ISO8859_6       = 'iso-8859-6'
    ISO8859_7       = 'iso-8859-7'
    ISO8859_8       = 'iso-8859-8'
    ISO8859_9       = 'iso-8859-9'
    ISO8859_10      = 'iso-8859-10'
    ISO8859_13      = 'iso-8859-13'
    ISO8859_14      = 'iso-8859-14'
    ISO8859_15      = 'iso-8859-15'

    JOHAB           = 'johab'
    KOI8_R          = 'koi8-r'
    KOI8_U          = 'koi8-u'

    MAC_CYRILLIC    = 'mac-cyrillic'
    MAC_GREEK       = 'mac-greek'
    MAC_ICELAND     = 'mac-iceland'
    MAC_LATIN2      = 'mac-latin2'
    MAC_ROMAN       = 'mac-roman'
    MAC_TURKISH     = 'mac-turkish'

    PTCP154         = 'ptcp154'
    SHIFT_JIS       = 'shift-jis'
    SHIFT_JIS_2004  = 'shift-jis_2004'
    SHIFT_JISX0213  = 'shift-jisx0213'

    UTF_16          = 'utf-16'
    UTF_16_BE       = 'utf-16-be'
    UTF_16_LE       = 'utf-16-le'
    UTF_7           = 'utf-7'
    UTF_8           = 'utf-8'

    # fmt: on

    @property
    def val(self) -> str:
        return str(self.value)
