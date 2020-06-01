from http.server import HTTPServer
from random import randint
from threading import Thread
from typing import Tuple, Optional

from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.enum.http_method import HttpMethod
from main.hspylib.modules.mock.mock_request import MockRequest
from main.hspylib.modules.mock.mock_server_handler import MockServerHandler


class MockServer(HTTPServer):

    RANDOM_PORT = randint(49152, 65535)

    def mock(self, method: HttpMethod, url: str) -> Optional[MockRequest]:
        try:
            return self.__mocks[method][url]
        except KeyError:
            return None

    def __init__(self, hostname: str, port: int):
        self.__mocks = {}
        self.hostname = hostname
        self.port = port
        self.version = '0.9.0'
        super().__init__(self.server_address(), MockServerHandler)

    def server_address(self) -> Tuple[str, int]:
        return self.hostname, self.port

    def is_allowed(self, method: HttpMethod):
        return method in self.__mocks

    def start(self):
        runner = ServerThread(self)
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


class ServerThread(Thread):
    def __init__(self, parent: MockServer):
        super().__init__()
        self.parent = parent

    def run(self) -> None:
        self.parent.serve_forever()


if __name__ == '__main__':
    server = MockServer('localhost', 3333)
    server\
        .when_request(HttpMethod.GET, '/')\
        .then_return(code=HttpCode.OK)
    server\
        .when_request(HttpMethod.POST, '/users')\
        .then_return_with_received_body(code=HttpCode.OK)
    server\
        .when_request(HttpMethod.PUT, '/users')\
        .then_return(code=HttpCode.OK, body='[{"name":"any-name"}]', headers=[{'Content-Length': '0'}, {'Etag': "3147526947"}])
    server.start()
