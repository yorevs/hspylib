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
        response = self.parent.mock(self.method, self.url)
        response.code = response_code
        response.body = response_body
        response.encoding = encoding
        response.content_type = content_type
        return self.parent
