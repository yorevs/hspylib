#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.fetch
      @file: fetch.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import Any, List, Optional, Tuple, Union

import requests
from requests import exceptions as ex

from hspylib.core.enums.http_code import HttpCode
from hspylib.core.enums.http_method import HttpMethod
from hspylib.core.tools.commons import sysout
from hspylib.modules.fetch.http_response import HttpResponse


def fetch(
    url: str,
    method: HttpMethod = HttpMethod.GET,
    headers: List[str] = None,
    body: Optional[Any] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> Optional[HttpResponse]:
    """ Do a request specified by method and according to parameters.
    :param url: The url to make the request.
    :param method: The http method to be used [ GET, HEAD, POST, PUT, PATCH, DELETE ].
    :param headers: The http request headers.
    :param body: The http request body (payload).
    :param silent: Omits all informational messages.
    :param timeout: How many seconds to wait for the server to send data or connect before giving up.
    :return:
    """

    url = url if url and url.startswith("http") else f'http://{url}'
    if not silent:
        sysout(f"Fetching: "
               f"method={method} table_headers={headers if headers else '[]'} "
               f"body={body if body else '{}'} url={url} ...")

    response = requests.request(
        url=url,
        method=method.name,
        headers=headers,
        data=body,
        timeout=timeout,
        verify=False)

    return HttpResponse.of(response)


def head(
    url: str,
    headers: List[str] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> Optional[HttpResponse]:
    """Do HEAD request and according to parameters."""

    return fetch(
        url=url,
        method=HttpMethod.HEAD,
        headers=headers,
        silent=silent,
        timeout=timeout)


def get(
    url: str,
    headers: List[str] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> Optional[HttpResponse]:
    """Do GET request and according to parameters."""

    return fetch(
        url=url,
        headers=headers,
        silent=silent,
        timeout=timeout)


def delete(
    url: str,
    headers: List[str] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> Optional[HttpResponse]:
    """Do DELETE request and according to parameters."""

    return fetch(
        url=url,
        method=HttpMethod.DELETE,
        headers=headers,
        silent=silent,
        timeout=timeout)


def post(
    url: str,
    body=None,
    headers: List[str] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> Optional[HttpResponse]:
    """Do POST request and according to parameters."""

    return fetch(
        url=url,
        method=HttpMethod.POST,
        headers=headers,
        body=body,
        silent=silent,
        timeout=timeout)


def put(
    url: str,
    body=None,
    headers: List[str] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> Optional[HttpResponse]:
    """Do PUT request and according to parameters."""

    return fetch(
        url=url,
        method=HttpMethod.PUT,
        headers=headers,
        body=body,
        silent=silent,
        timeout=timeout)


def patch(
    url: str,
    body=None,
    headers: List[str] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> Optional[HttpResponse]:
    """Do PATCH request and according to parameters."""

    return fetch(
        url=url,
        method=HttpMethod.PATCH,
        headers=headers,
        body=body,
        silent=silent,
        timeout=timeout)


def is_reachable(
    url: str,
    timeout: Union[float, Tuple[float, float]] = 1) -> bool:
    """Check if the specified url is reachable"""

    try:
        resp = fetch(url=url, method=HttpMethod.HEAD, timeout=timeout)
        return HttpCode.OK.value <= resp.status_code.value < HttpCode.MULTIPLE_CHOICES.value
    except (ex.ConnectTimeout, ex.ConnectionError, ex.ReadTimeout, ex.InvalidURL):
        return False
