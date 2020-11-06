from hspylib.core.enum.charset import Charset
from hspylib.core.enum.content_type import ContentType
from hspylib.core.enum.http_code import HttpCode
from hspylib.core.enum.http_method import HttpMethod
from requests.models import Response, CaseInsensitiveDict


class HttpResponse:
    @staticmethod
    def of(response: Response):
        return HttpResponse(
            HttpMethod[response.request.method],
            response.url,
            HttpCode(response.status_code),
            response.text,
            response.headers,
            Charset(str(response.encoding).upper()) if response.encoding else None,
        )

    def __init__(self,
                 method: HttpMethod,
                 url: str,
                 status_code: HttpCode = None,
                 body: str = None,
                 headers: CaseInsensitiveDict = None,
                 encoding: Charset = Charset.UTF_8,
                 content_type=ContentType.APPLICATION_JSON):
        self.method = method
        self.url = url
        self.status_code = status_code
        self.body = body
        self.headers = headers
        self.encoding = encoding
        self.content_type = content_type
        if self.content_type:
            self.content_type.charset = self.encoding
