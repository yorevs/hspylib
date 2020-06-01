from http.server import BaseHTTPRequestHandler
from typing import Tuple, List, Dict

from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.enum.http_method import HttpMethod
from main.hspylib.modules.mock.mock_request import MockRequest


class MockServerHandler(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: Tuple[str, int], parent):
        self.parent = parent
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

    def process_default(self,
                        code: HttpCode = HttpCode.OK,
                        content_type: str = 'text/plain; charset=utf-8',
                        headers: List[Dict[str, str]] = None):
        self.send_response(code.value)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", '0')
        if headers and len(headers) > 0:
            for header in headers:
                for key, value in header.items():
                    self.send_header(key, value)
        self.end_headers()

    def find_allowed_methods(self):
        allowed_methods = ['OPTIONS']
        if self.parent.is_mocked(HttpMethod.HEAD):
            allowed_methods.append('HEAD')
        if self.parent.is_mocked(HttpMethod.GET):
            allowed_methods.append('GET')
        if self.parent.is_mocked(HttpMethod.POST):
            allowed_methods.append('POST')
        if self.parent.is_mocked(HttpMethod.PUT):
            allowed_methods.append('PUT')
        if self.parent.is_mocked(HttpMethod.PATCH):
            allowed_methods.append('PATCH')
        if self.parent.is_mocked(HttpMethod.DELETE):
            allowed_methods.append('DELETE')
        return allowed_methods

    def do_HEAD(self):
        mock_request = self.parent.mock(HttpMethod.HEAD, self.path)
        if mock_request:
            mock_request.body = None
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.METHOD_NOT_ALLOWED)

    def do_OPTIONS(self):
        mock_request = self.parent.mock(HttpMethod.OPTIONS, self.path)
        headers = [
            {'Allow': ', '.join(self.find_allowed_methods())}
        ]
        if mock_request:
            mock_request.body = None
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.NO_CONTENT, headers=headers)

    def do_GET(self):
        mock_request = self.parent.mock(HttpMethod.GET, self.path)
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.METHOD_NOT_ALLOWED)

    def do_POST(self):
        mock_request = self.parent.mock(HttpMethod.POST, self.path)
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.METHOD_NOT_ALLOWED)

    def do_PUT(self):
        mock_request = self.parent.mock(HttpMethod.PUT, self.path)
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.METHOD_NOT_ALLOWED)

    def do_PATCH(self):
        mock_request = self.parent.mock(HttpMethod.PATCH, self.path)
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.METHOD_NOT_ALLOWED)

    def do_DELETE(self):
        mock_request = self.parent.mock(HttpMethod.DELETE, self.path)
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.METHOD_NOT_ALLOWED)
