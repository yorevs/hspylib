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

   Copyright 2022, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration


class HttpMethod(Enumeration):
    """Associates the name of a HTTP method with an enumeration."""

    # fmt: off

    # The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
    GET         = 'get'

    # The HEAD method asks for a response identical to a GET request, but without the response body.
    HEAD        = 'head'

    # The POST method submits an entity to the specified resource, often causing a change in state or side effects
    # on the server.
    POST        = 'post'

    # The PUT method replaces all current representations of the target resource with the request payload.
    PUT         = 'put'

    # The DELETE method deletes the specified resource.
    DELETE      = 'delete'

    # The CONNECT method establishes a tunnel to the server identified by the target resource.
    CONNECT     = 'connect'

    # The OPTIONS method describes the communication options for the target resource.
    OPTIONS     = 'options'

    # The TRACE method performs a message loop-back test along the path to the target resource.
    TRACE       = 'trace'

    # The PATCH method applies partial modifications to a resource.
    PATCH       = 'patch'

    # fmt: on

    @property
    def val(self) -> str:
        return str(self.value)
