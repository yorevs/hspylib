#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.mock
      @file: mock_server.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from http.server import HTTPServer
from random import randint
from threading import Thread
from time import sleep
from typing import Optional, Tuple

from requests.structures import CaseInsensitiveDict

from hspylib.core.enums.charset import Charset
from hspylib.core.enums.content_type import ContentType
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.enums.http_method import HttpMethod
from hspylib.modules.fetch.http_response import HttpResponse
from hspylib.modules.mock.mock_server_handler import MockServerHandler


class MockServer(HTTPServer):
    """TODO"""

    RANDOM_PORT = randint(49152, 65535)

    class ServerThread(Thread):
        def __init__(self, parent: 'MockServer'):
            super().__init__()
            self.parent = parent

        def run(self) -> None:
            self.parent.serve_forever()

    class MockResponse(HttpResponse):
        """TODO"""

        def __init__(
            self,
            parent: 'MockServer',
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

        def then_wait(self, delay: int) -> 'MockServer.MockResponse':
            sleep(delay)
            return self

        def then_return(
            self,
            code: HttpCode,
            body: str = None,
            headers=None,
            encoding: Charset = Charset.UTF_8,
            content_type=ContentType.APPLICATION_JSON) -> 'MockServer':
            """TODO"""

            response = self.parent.mock(self.method, self.url)
            response.status_code = code
            response.body = body
            response.headers = headers if headers else []
            response.encoding = encoding
            response.content_type = content_type
            if response.content_type:
                response.content_type.charset = encoding

            return self.parent

        def then_return_with_received_body(
            self,
            code: HttpCode,
            headers: CaseInsensitiveDict = None,
            encoding: Charset = Charset.UTF_8,
            content_type=ContentType.APPLICATION_JSON) -> 'MockServer':
            """TODO"""

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

    def __init__(self, hostname: str, port: int):
        self._mocks = {}
        self.hostname = hostname
        self.port = port
        self.version = '0.9.0'
        super().__init__(self.address(), MockServerHandler)

    def mock(self, method: HttpMethod, url: str) -> Optional[MockResponse]:
        """TODO"""
        try:
            return self._mocks[method][url]
        except KeyError:
            return None

    def address(self) -> Tuple[str, int]:
        """TODO"""
        return self.hostname, self.port

    def is_allowed(self, method: HttpMethod) -> bool:
        """TODO"""
        return method in self._mocks

    def start(self) -> None:
        """TODO"""
        runner = self.ServerThread(self)
        runner.start()

    def stop(self) -> None:
        """TODO"""
        self.shutdown()
        self.server_close()

    def when_request(self, method: HttpMethod, url: str) -> Optional[MockResponse]:
        """TODO"""
        request = self.mock(method=method, url=url) or self.MockResponse(self, method, url)
        self._mocks[method] = self._mocks[method] if method in self._mocks else {}
        self._mocks[method][url] = request
        return request
