#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.core
      @file: constants.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

# Commonly used regex expressions

# fmt: off

TRUE_VALUES = {"true", "on", "yes", "y", "1"}

# Regex expressions

UL = "\u00a1-\uffff"  # Unicode letters range (must not be a raw string).

RE_UUID = r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"

RE_PHONE_NUMBER = r"((\d{2})?\s)?(\d{4,5}\-?\d{4})"

RE_COMMON_2_30_NAME = r"[a-zA-Z][\w]{2,30}"

RE_EMAIL_W3C = r"^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"

RE_IPV4 = (
    r"(?:0|25[0-5]|2[0-4][0-9]|1[0-9]?[0-9]?|[1-9][0-9]?)"
    r"(?:\.(?:0|25[0-5]|2[0-4][0-9]|1[0-9]?[0-9]?|[1-9][0-9]?)){3}"
)

RE_IPV6 = r"\[[0-9a-f:.]+\]"

RE_HOSTNAME = r"[a-z" + UL + r"0-9](?:[a-z" + UL + r"0-9-]{0,61}[a-z" + UL + r"0-9])?"

RE_DOMAIN = r"(?:\.(?!-)[a-z" + UL + r"0-9-]{1,63}(?<!-))*"

TLD_RE = (
    r"\."  # dot
    r"(?!-)"  # can't start with a dash
    r"(?:[a-z" + UL + "-]{2,63}"  # domain label
    r"|xn--[a-z0-9]{1,59})"  # or punycode label
    r"(?<!-)"  # can't end with a dash
    r"\.?"  # may have a trailing dot
)

RE_CNPJ = r"^(\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2})$"

RE_HOST = "(" + RE_HOSTNAME + RE_DOMAIN + TLD_RE + "|localhost)"

RE_URL = (
    r"^(?:[a-z0-9.+-]*)://"  # scheme is validated separately
    r"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"  # user:pass authentication
    r"(?:" + RE_IPV4 + "|" + RE_IPV6 + "|" + RE_HOST + ")"
    r"(?::[0-9]{1,5})?"  # port
    r"(?:[/?#][^\s]*)?"  # resource path
    r"\Z"
)

# fmt: on
