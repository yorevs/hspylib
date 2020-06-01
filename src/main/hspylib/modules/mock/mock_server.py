import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from typing import Tuple, Optional

from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.enum.http_method import HttpMethod


class MockRequest:
    def __init__(self,
                 parent,
                 method: HttpMethod,
                 url: str,
                 code: HttpCode = None,
                 body: str = None,
                 encoding: str = 'utf-8',
                 content_type='application/json'):
        self.parent = parent
        self.method = method
        self.url = url
        self.code = code
        self.body = body
        self.encoding = encoding
        self.content_type = content_type

    def then_return(self,
                    response_code: HttpCode,
                    response_body: str = None,
                    encoding: str = 'utf-8',
                    content_type: str = 'application/json'):
        response = MockServer.mock(self.method, self.url)
        response.code = response_code
        response.body = response_body
        response.encoding = encoding
        response.content_type = content_type
        return self.parent


class MockServerHandler(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: Tuple[str, int], parent: socketserver.BaseServer):
        super().__init__(request, client_address, parent)

    def process_request(self, mock_request: MockRequest):
        code = mock_request.code.value if mock_request.code else HttpCode.INTERNAL_SERVER_ERROR.value
        self.send_response(code)
        self.send_header("Content-type", "{}; charset={}".format(
            mock_request.content_type, mock_request.encoding))
        self.send_header("Content-Length", str(len(mock_request.body) if mock_request.body else 0))
        self.end_headers()
        if mock_request.body:
            self.wfile.write(mock_request.body.encode(mock_request.encoding))

    def process_default(self, code: HttpCode = HttpCode.OK):
        self.send_response(code.value)
        self.send_header("Content-type", 'text/plain; charset=utf-8')
        self.send_header("Content-Length", '0')
        self.end_headers()

    def do_HEAD(self):
        mock_request = MockServer.mock(HttpMethod.HEAD, self.path)
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default()

    def do_GET(self):
        mock_request = MockServer.mock(HttpMethod.GET, self.path)
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.NOT_FOUND)

    def do_POST(self):
        mock_request = MockServer.mock(HttpMethod.POST, self.path)
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.NOT_FOUND)

    def do_PUT(self):
        mock_request = MockServer.mock(HttpMethod.PUT, self.path)
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.NOT_FOUND)

    def do_PATCH(self):
        mock_request = MockServer.mock(HttpMethod.PATCH, self.path)
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.NOT_FOUND)

    def do_DELETE(self):
        mock_request = MockServer.mock(HttpMethod.DELETE, self.path)
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.NOT_FOUND)


class MockServer(HTTPServer):
    __mocks = {}

    @staticmethod
    def mock(method: HttpMethod, url: str) -> Optional[MockRequest]:
        try:
            return MockServer.__mocks[method][url]
        except KeyError:
            return None

    class ServerThread(Thread):
        def __init__(self, server):
            super().__init__()
            self.server = server

        def run(self) -> None:
            self.server.serve_forever()

    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port
        super().__init__(self.server_address(), MockServerHandler)

    def server_address(self) -> Tuple[str, int]:
        return self.hostname, self.port

    def start(self):
        runner = MockServer.ServerThread(self)
        runner.start()

    def stop(self):
        self.shutdown()
        self.server_close()

    def when_request(self, method: HttpMethod, url: str):
        request = MockServer.mock(method=method, url=url) or MockRequest(self, method, url)
        MockServer.__mocks[method] = MockServer.__mocks[method] \
            if method in MockServer.__mocks else {}
        MockServer.__mocks[method][url] = request
        return request
