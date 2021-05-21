#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.mock
      @file: mock_request.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from typing import Any

from requests.structures import CaseInsensitiveDict

from hspylib.core.enums.charset import Charset
from hspylib.core.enums.content_type import ContentType
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.enums.http_method import HttpMethod
from hspylib.modules.fetch.http_response import HttpResponse


class MockResponse(HttpResponse):
    def __init__(self,
                 parent,
                 method: HttpMethod,
                 url: str,
                 status_code: HttpCode = None,
                 body: str = None,
                 headers=None,
                 encoding: Charset = Charset.UTF_8,
                 content_type=ContentType.APPLICATION_JSON):
        
        super().__init__(method, url, status_code, body, headers, encoding, content_type)
        self.parent = parent
        self.received_body = False
    
    def then_return(self,
                    code: HttpCode,
                    body: str = None,
                    headers=None,
                    encoding: Charset = Charset.UTF_8,
                    content_type=ContentType.APPLICATION_JSON) -> Any:
        
        response = self.parent.mock(self.method, self.url)
        response.status_code = code
        response.body = body
        response.headers = headers if headers else []
        response.encoding = encoding
        response.content_type = content_type
        if response.content_type:
            response.content_type.charset = encoding
        return self.parent
    
    def then_return_with_received_body(self,
                                       code: HttpCode,
                                       headers: CaseInsensitiveDict = None,
                                       encoding: Charset = Charset.UTF_8,
                                       content_type=ContentType.APPLICATION_JSON) -> Any:
        response = self.parent.mock(self.method, self.url)
        response.received_body = True
        response.body = None
        response.status_code = code
        response.headers = headers if headers else []
        response.encoding = encoding
        response.content_type = content_type
        if response.content_type:
            response.content_type.charset = encoding
        return self.parent
