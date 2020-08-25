import logging as log
from enum import Enum
from typing import Optional

import requests
from requests.structures import CaseInsensitiveDict


def soap_call(
        url: str,
        method: str,
        data: str,
        headers: Optional[CaseInsensitiveDict]) -> requests.Response:
    all_headers = {} if not headers else headers
    all_headers.update({
        "Content-Type": "text/xml",
        "Accept": "*/*"
    })
    log.info('Processing SOAP {} {} -> {} \n{}'.format(all_headers, method, url, data if data else ''))
    response = requests.request(url=url, method=method, headers=all_headers, data=data)
    log.info('Response <=  Status: {}  Payload: {}'
         .format(response.status_code, response.content if response.content else '<None>'))

    return response
