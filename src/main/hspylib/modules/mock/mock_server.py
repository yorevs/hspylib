#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.mock
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
from typing import Any, Optional, Tuple

from hspylib.core.enums.http_method import HttpMethod
from hspylib.modules.mock.mock_request import MockResponse
from hspylib.modules.mock.mock_server_handler import MockServerHandler


class MockServer(HTTPServer):
    RANDOM_PORT = randint(49152, 65535)
    
    def mock(self, method: HttpMethod, url: str) -> Optional[MockResponse]:
        try:
            return self.__mocks[method][url]
        except KeyError:
            return None
    
    def __init__(self, hostname: str, port: int):
        self.__mocks = {}
        self.hostname = hostname
        self.port = port
        self.version = '0.9.0'
        super().__init__(self.address(), MockServerHandler)
    
    def address(self) -> Tuple[str, int]:
        return self.hostname, self.port
    
    def is_allowed(self, method: HttpMethod) -> bool:
        return method in self.__mocks
    
    def start(self) -> None:
        runner = ServerThread(self)
        runner.start()
    
    def stop(self) -> None:
        self.shutdown()
        self.server_close()
    
    def when_request(self, method: HttpMethod, url: str) -> Any:
        request = self.mock(method=method, url=url) or MockResponse(self, method, url)
        self.__mocks[method] = self.__mocks[method] \
            if method in self.__mocks else {}
        self.__mocks[method][url] = request
        return request


class ServerThread(Thread):
    def __init__(self, parent: MockServer):
        super().__init__()
        self.parent = parent
    
    def run(self) -> None:
        self.parent.serve_forever()
