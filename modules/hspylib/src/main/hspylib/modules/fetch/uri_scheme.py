#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: hspylib
   @package: hspylib.modules.fetch
      @file: uri_scheme.py
   @created: Mon, 12 Dec 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration


class UriScheme(Enumeration):
    """Uniform Resource Identifier helps identify a source without ambiguity
    Ref.: https://en.wikipedia.org/wiki/List_of_URI_schemes
    """

    # fmt: off
    ABOUT   = 'about'
    HTTP    = 'http'
    HTTPS   = 'https'
    FTP     = 'ftp'
    FILE    = 'file'
    # fmt: on

    @classmethod
    def of(cls, scheme: str) -> "UriScheme":
        try:
            e = super().of_value(scheme, ignore_case=True)
            return e
        except TypeError as err:
            raise NotImplementedError(f"'{scheme}' scheme is not supported") from err
