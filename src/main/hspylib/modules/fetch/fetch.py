#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.fetch
      @file: fetch.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any, Optional

import requests

from hspylib.core.enums.http_method import HttpMethod
from hspylib.core.tools.commons import sysout
from hspylib.modules.fetch.http_response import HttpResponse


def fetch(
        url: str,
        method: HttpMethod = HttpMethod.GET,
        headers: list = None,
        body: Optional[Any] = None,
        silent=True) -> Optional[HttpResponse]:
    """ Do a request specified by method and according to parameters.
    :param url: The url to make the request.
    :param method: The http method to be used [ GET, HEAD, POST, PUT, PATCH, DELETE ].
    :param headers: The http request headers.
    :param body: The http request body (payload).
    :param silent: Omits all informational messages.
    :return:
    """
    
    url = url if url and url.startswith("http") else 'http://{}'.format(url)
    if not silent:
        sysout('Fetching: method={} table_headers={} body={} url={} ...'.format(
            method, headers if headers else '[]', body if body else '{}', url))
    response = requests.request(url=url, method=method.name, headers=headers, data=body, timeout=3)
    return HttpResponse.of(response)


def head(url: str, headers=None, silent=True) -> Optional[HttpResponse]:
    """Do HEAD request and according to parameters."""
    return fetch(url=url, method=HttpMethod.HEAD, headers=headers, silent=silent)


def get(url: str, headers=None, silent=True) -> Optional[HttpResponse]:
    """Do GET request and according to parameters."""
    return fetch(url=url, headers=headers, silent=silent)


def delete(url: str, headers=None, silent=True) -> Optional[HttpResponse]:
    """Do DELETE request and according to parameters."""
    return fetch(url=url, method=HttpMethod.DELETE, headers=headers, silent=silent)


def post(url: str, body=None, headers=None, silent=True) -> Optional[HttpResponse]:
    """Do POST request and according to parameters."""
    return fetch(url, HttpMethod.POST, headers, body, silent)


def put(url, body=None, headers=None, silent=True) -> Optional[HttpResponse]:
    """Do PUT request and according to parameters."""
    return fetch(url=url, method=HttpMethod.PUT, headers=headers, body=body, silent=silent)


def patch(url, body=None, headers=None, silent=True) -> Optional[HttpResponse]:
    """Do PATCH request and according to parameters."""
    return fetch(url=url, method=HttpMethod.PATCH, headers=headers, body=body, silent=silent)
