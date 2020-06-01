from http.server import BaseHTTPRequestHandler
from typing import Tuple, List, Dict

from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.enum.http_method import HttpMethod


class MockServerHandler(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: Tuple[str, int], parent):
        self.parent = parent
        super().__init__(request, client_address, parent)

    @staticmethod
    def remove_reserved_headers(headers: List[Dict[str, str]]):
        filtered = []
        if headers:
            reserved = ['content-type', 'content-length', 'server', 'date']
            for header in headers:
                for key in header:
                    if key.lower() not in reserved:
                        filtered.append(header)
        return filtered

    def process_headers(self,
                        headers: List[Dict[str, str]] = None,
                        content_type: str = 'text/plain; charset=UTF-8',
                        content_length: int = 0):
        headers = MockServerHandler.remove_reserved_headers(headers)
        if headers and len(headers) > 0:
            for header in headers:
                for key, value in header.items():
                    self.send_header(key, value)
        self.send_header("Server", 'MockServer v{}'.format(self.parent.version))
        self.send_header("Date", self.date_time_string())
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(content_length))
        self.end_headers()

    def process_default(self,
                        code: HttpCode = HttpCode.OK,
                        content_type: str = 'text/plain; charset=utf-8',
                        headers: List[Dict[str, str]] = None):
        self.send_response_only(code.value)
        self.process_headers(headers, content_type)

    def process_request(self, method: HttpMethod):
        if self.parent.is_allowed(method):
            request = self.parent.mock(method, self.path)
            if request:
                if not request.code:
                    code = HttpCode.INTERNAL_SERVER_ERROR.value
                    request.body = 'Mocked response code must be provided'
                elif method in ['OPTIONS', 'HEAD']:
                    code = request.code.value
                    request.body = None
                else:
                    code = request.code.value
                headers = request.headers if request.headers else []
                self.send_response_only(code)
                if request.received_body:
                    length = int(self.headers['Content-Length'])
                    request.body = self.rfile.read(length).decode(request.encoding)
                    self.process_headers(headers, request.content_type, length)
                else:
                    self.process_headers(headers, request.content_type, len(request.body) if request.body else 0)
                if request.body:
                    self.wfile.write(request.body.encode(request.encoding))
            else:
                self.process_default(HttpCode.NOT_FOUND)
        else:
            self.process_default(HttpCode.METHOD_NOT_ALLOWED)

    def find_allowed_methods(self):
        allowed_methods = ['OPTIONS']
        if self.parent.is_allowed(HttpMethod.HEAD):
            allowed_methods.append('HEAD')
        if self.parent.is_allowed(HttpMethod.GET):
            allowed_methods.append('GET')
        if self.parent.is_allowed(HttpMethod.POST):
            allowed_methods.append('POST')
        if self.parent.is_allowed(HttpMethod.PUT):
            allowed_methods.append('PUT')
        if self.parent.is_allowed(HttpMethod.PATCH):
            allowed_methods.append('PATCH')
        if self.parent.is_allowed(HttpMethod.DELETE):
            allowed_methods.append('DELETE')
        return allowed_methods

    def do_OPTIONS(self):
        mock_request = self.parent.mock(HttpMethod.OPTIONS, self.path)
        headers = [
            {'Allow': ', '.join(self.find_allowed_methods())}
        ]
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.NO_CONTENT, headers=headers)

    def do_HEAD(self):
        self.process_request(HttpMethod.HEAD)

    def do_GET(self):
        self.process_request(HttpMethod.GET)

    def do_POST(self):
        self.process_request(HttpMethod.POST)

    def do_PUT(self):
        self.process_request(HttpMethod.PUT)

    def do_PATCH(self):
        self.process_request(HttpMethod.PATCH)

    def do_DELETE(self):
        self.process_request(HttpMethod.DELETE)
