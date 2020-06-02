from requests.models import Response, CaseInsensitiveDict

from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.enum.http_method import HttpMethod


class HttpResponse:
    @staticmethod
    def of(response: Response):
        return HttpResponse(
            HttpMethod[response.request.method],
            response.url,
            HttpCode(response.status_code),
            response.text,
            response.headers,
            response.encoding,
        )

    def __init__(self,
                 method: HttpMethod,
                 url: str,
                 status_code: HttpCode = None,
                 body: str = None,
                 headers: CaseInsensitiveDict = None,
                 encoding: str = 'UTF-8',
                 content_type='application/json; charset=UTF-8'):
        self.method = method
        self.url = url
        self.status_code = status_code
        self.body = body
        self.headers = headers
        self.encoding = encoding
        self.content_type = content_type
