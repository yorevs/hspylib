import signal
from http.server import HTTPServer
from threading import Thread
from typing import Tuple, Optional

from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.enum.http_method import HttpMethod
from main.hspylib.modules.mock.mock_request import MockRequest
from main.hspylib.modules.mock.mock_server_handler import MockServerHandler


class MockServer(HTTPServer):

    def mock(self, method: HttpMethod, url: str) -> Optional[MockRequest]:
        try:
            return self.__mocks[method][url]
        except KeyError:
            return None

    class ServerThread(Thread):
        def __init__(self, server):
            super().__init__()
            self.server = server

        def run(self) -> None:
            self.server.serve_forever()

    def __init__(self, hostname: str, port: int):
        self.__mocks = {}
        self.hostname = hostname
        self.port = port
        super().__init__(self.server_address(), MockServerHandler)

    def server_address(self) -> Tuple[str, int]:
        return self.hostname, self.port

    def is_mocked(self, method: HttpMethod):
        return method in self.__mocks

    def start(self):
        runner = MockServer.ServerThread(self)
        runner.start()

    def stop(self):
        self.shutdown()
        self.server_close()

    def when_request(self, method: HttpMethod, url: str):
        request = self.mock(method=method, url=url) or MockRequest(self, method, url)
        self.__mocks[method] = self.__mocks[method] \
            if method in self.__mocks else {}
        self.__mocks[method][url] = request
        return request
