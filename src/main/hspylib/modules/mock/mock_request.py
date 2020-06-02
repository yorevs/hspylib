from requests.structures import CaseInsensitiveDict

from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.enum.http_method import HttpMethod
from main.hspylib.modules.fetch.http_response import HttpResponse


class MockResponse(HttpResponse):
    def __init__(self,
                 parent,
                 method: HttpMethod,
                 url: str,
                 status_code: HttpCode = None,
                 body: str = None,
                 headers: CaseInsensitiveDict = None,
                 encoding: str = 'UTF-8',
                 content_type='application/json; charset=UTF-8'):

        super().__init__(method, url, status_code, body, headers, encoding, content_type)
        self.parent = parent
        self.received_body = False

    def then_return(self,
                    code: HttpCode,
                    body: str = None,
                    headers: CaseInsensitiveDict = None,
                    encoding: str = 'UTF-8',
                    content_type: str = 'application/json; charset=UTF-8'):

        response = self.parent.mock(self.method, self.url)
        response.status_code = code
        response.body = body
        response.headers = headers if headers else []
        response.encoding = encoding
        response.content_type = content_type
        return self.parent

    def then_return_with_received_body(self,
                                       code: HttpCode,
                                       headers: CaseInsensitiveDict = None,
                                       encoding: str = 'UTF-8',
                                       content_type: str = 'application/json; charset=UTF-8'):
        response = self.parent.mock(self.method, self.url)
        response.received_body = True
        response.body = None
        response.status_code = code
        response.headers = headers if headers else []
        response.encoding = encoding
        response.content_type = content_type
        return self.parent
