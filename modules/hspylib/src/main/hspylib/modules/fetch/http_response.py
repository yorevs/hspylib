#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.fetch
      @file: http_response.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from hspylib.core.enums.charset import Charset
from hspylib.core.enums.content_type import ContentType
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.enums.http_method import HttpMethod
from requests.models import CaseInsensitiveDict, Response
from typing import Optional


class HttpResponse:
    """Class that represents an HTTP status."""

    @staticmethod
    def of(response: Response) -> "HttpResponse":
        """Create an HTTP status based on a Requests.Response object."""
        return HttpResponse(
            HttpMethod.value_of(response.request.method),
            response.url,
            HttpCode.of(response.status_code),
            response.headers,
            response.text,
            Charset.of_value(response.encoding.lower()) if response.encoding else Charset.UTF_8,
        )

    def __init__(
        self,
        method: HttpMethod,
        url: str,
        status_code: HttpCode,
        headers: CaseInsensitiveDict = None,
        body: Optional[str] = None,
        encoding: Charset = Charset.UTF_8,
        content_type=ContentType.APPLICATION_JSON,
    ):
        self.method = method
        self.url = url
        self.status_code = status_code
        self.body = body
        self.headers = headers
        self.encoding = encoding
        self.content_type = content_type
        if self.content_type:
            self.content_type.charset = self.encoding

    def __repr__(self):
        return f"{repr(self.status_code)} {self.url}"
