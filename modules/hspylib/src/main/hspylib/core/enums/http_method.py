#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.enum
      @file: http_method.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration


class HttpMethod(Enumeration):
    """TODO"""

    # @formatter:off
    OPTIONS     = 'options'
    HEAD        = 'head'
    GET         = 'get'
    POST        = 'post'
    PUT         = 'put'
    PATCH       = 'patch'
    DELETE      = 'delete'
    # @formatter:on
