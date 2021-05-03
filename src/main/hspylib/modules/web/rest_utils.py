import logging as log
from typing import Optional

from requests.structures import CaseInsensitiveDict

from hspylib.core.enum.http_method import HttpMethod
from hspylib.modules.fetch.fetch import fetch
from hspylib.modules.fetch.http_response import HttpResponse


def rest_call(
        url: str,
        method: HttpMethod,
        data: str,
        headers: Optional[CaseInsensitiveDict]) -> Optional[HttpResponse]:

    all_headers = {} if not headers else headers
    all_headers.update({
        "Content-Type": "text/json",
        "Accept": "*/*"
    })
    log.info('Processing REST {} {} -> {}'.format(all_headers, method, url))
    response = fetch(url=url, method=method, headers=all_headers, body=data)
    log.info('Response <=  Status: {}  Payload: {}'.format(
        response.status_code, response))

    return response
