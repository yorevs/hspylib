#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.fetch
      @file: http_response.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from requests.models import CaseInsensitiveDict, Response

from hspylib.core.enums.charset import Charset
from hspylib.core.enums.content_type import ContentType
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.enums.http_method import HttpMethod


class HttpResponse:
    """TODO"""

    @staticmethod
    def of(response: Response) -> 'HttpResponse':
        """TODO"""
        return HttpResponse(
            HttpMethod[response.request.method],
            response.url,
            HttpCode(response.status_code),
            response.text,
            response.headers,
            Charset(str(response.encoding).upper()) if response.encoding else None,
        )

    def __init__(
        self,
        method: HttpMethod,
        url: str,
        status_code: HttpCode = None,
        body: str = None,
        headers: CaseInsensitiveDict = None,
        encoding: Charset = Charset.UTF_8,
        content_type=ContentType.APPLICATION_JSON):
        self.method = method
        self.url = url
        self.status_code = status_code
        self.body = body
        self.headers = headers
        self.encoding = encoding
        self.content_type = content_type
        if self.content_type:
            self.content_type.charset = self.encoding

    def __str__(self):
        return f"({self.status_code.value}) {self.status_code} {self.url}"

    def __repr__(self):
        return str(self.status_code.value)
