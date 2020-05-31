import socketserver
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Tuple


class ServerMock(HTTPServer):

    class RequestHandler(SimpleHTTPRequestHandler):
        def __init__(self, request: bytes, client_address: Tuple[str, int], parent: socketserver.BaseServer):
            super().__init__(request, client_address, parent)

    class Builder:
        def __init__(self):
            self.port = 333
            self.hostname = 'localhost'

        def with_port(self, port: int):
            self.port = port
            return self

        def with_hostname(self, hostname: str):
            self.hostname = hostname
            return self

        def build(self):
            return ServerMock(self.hostname, self.port)

    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port
        super().__init__(self.server_address(), ServerMock.RequestHandler)

    def server_address(self) -> Tuple[str, int]:
        return self.hostname, self.port

    def start(self):
        self.serve_forever(1000)


server = ServerMock('localhost', 8080)
server.start()
