#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.main.hspylib.modules.web
      @file: rest_utils.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
from typing import Optional

from requests.structures import CaseInsensitiveDict

from hspylib.core.enums.http_method import HttpMethod
from hspylib.modules.fetch.fetch import fetch
from hspylib.modules.fetch.http_response import HttpResponse


def rest_call(
        url: str,
        method: HttpMethod,
        data: str,
        headers: Optional[CaseInsensitiveDict]) -> Optional[HttpResponse]:
    """TODO"""

    all_headers = {} if not headers else headers
    all_headers.update({
        "Content-Type": "text/json",
        "Accept": "*/*"
    })
    log.info('Processing REST {all_headers} {method} -> {url}')
    response = fetch(url=url, method=method, headers=all_headers, body=data)
    log.info(f"Response <=  Status: {response.status_code}  Payload: {response}")

    return response
