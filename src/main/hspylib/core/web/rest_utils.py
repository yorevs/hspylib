import logging as log
from typing import Optional

import requests
from requests.structures import CaseInsensitiveDict


def rest_call(
        url: str,
        method: str,
        data: str,
        headers: Optional[CaseInsensitiveDict]):
    all_headers = {} if not headers else headers
    all_headers.update({
        "Content-Type": "text/json",
        "Accept": "*/*"
    })
    log.info('Processing REST {} {} -> {}'.format(all_headers, method, url))
    response = requests.request(url=url, method=method, headers=all_headers, data=data)
    log.info('Response <=  Status: {}  Payload: {}'.format(response.status_code, response))

    return response
