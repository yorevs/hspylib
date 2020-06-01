from typing import List, Dict

from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.enum.http_method import HttpMethod


class MockRequest:
    def __init__(self,
                 parent,
                 method: HttpMethod,
                 url: str,
                 code: HttpCode = None,
                 body: str = None,
                 headers: list = None,
                 encoding: str = 'utf-8',
                 content_type='application/json'):
        self.parent = parent
        self.method = method
        self.url = url
        self.code = code
        self.body = body
        self.headers = headers
        self.encoding = encoding
        self.content_type = content_type
        self.received_body = False

    def then_return(self,
                    code: HttpCode,
                    body: str = None,
                    headers: List[Dict[str, str]] = None,
                    encoding: str = 'utf-8',
                    content_type: str = 'application/json; charset={}'):
        response = self.parent.mock(self.method, self.url)
        response.code = code
        response.body = body
        response.headers = headers if headers else []
        response.encoding = encoding
        response.content_type = content_type
        return self.parent

    def then_return_with_received_body(self,
                                       code: HttpCode,
                                       headers: List[Dict[str, str]] = None,
                                       encoding: str = 'utf-8',
                                       content_type: str = 'application/json; charset={}'):
        response = self.parent.mock(self.method, self.url)
        response.received_body = True
        response.body = None
        response.code = code
        response.headers = headers if headers else []
        response.encoding = encoding
        response.content_type = content_type
        return self.parent
