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

from typing import Any, Dict, List, Tuple, Union

import requests
from requests import exceptions as ex
from retry import retry

from hspylib.core.enums.http_method import HttpMethod
from hspylib.core.tools.commons import sysout
from hspylib.modules.fetch.http_response import HttpResponse


@retry(tries=3, delay=1, backoff=3, max_delay=30, jitter=0.75)
def fetch(
    url: str,
    method: HttpMethod = HttpMethod.GET,
    headers: List[Dict[str, str]] = None,
    body: Any = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> HttpResponse:
    """ Do a request specified by method and according to parameters.
    :param url: The url to make the request.
    :param method: The http method to be used [ GET, HEAD, POST, PUT, PATCH, DELETE, OPTIONS ].
    :param headers: The http request headers.
    :param body: The http request body (payload).
    :param silent: Omits all informational messages.
    :param timeout: How many seconds to wait for the server to send data or connect before giving up.
    :return:
    """

    url = url if url and url.startswith("http") else f'http://{url}'
    if not silent:
        sysout(f"Fetching: "
               f"method={method} headers={headers if headers else '[]'} "
               f"body={body if body else '{}'} url={url} ...")

    all_headers = {}
    if headers:
        list(map(all_headers.update, headers))

    response = requests.request(
        url=url,
        method=method.name,
        headers=all_headers,
        data=body,
        timeout=timeout,
        verify=False)

    return HttpResponse.of(response)


def head(
    url: str,
    headers: List[Dict[str, str]] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> HttpResponse:
    """Do HEAD request and according to parameters."""

    return fetch(
        url=url,
        method=HttpMethod.HEAD,
        headers=headers,
        silent=silent,
        timeout=timeout)


def get(
    url: str,
    headers: List[Dict[str, str]] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> HttpResponse:
    """Do GET request and according to parameters."""

    return fetch(
        url=url,
        headers=headers,
        silent=silent,
        timeout=timeout)


def delete(
    url: str,
    headers: List[Dict[str, str]] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> HttpResponse:
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
    headers: List[Dict[str, str]] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> HttpResponse:
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
    headers: List[Dict[str, str]] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> HttpResponse:
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
    headers: List[Dict[str, str]] = None,
    silent: bool = True,
    timeout: Union[float, Tuple[float, float]] = 10) -> HttpResponse:
    """Do PATCH request and according to parameters."""

    return fetch(
        url=url,
        method=HttpMethod.PATCH,
        headers=headers,
        body=body,
        silent=silent,
        timeout=timeout)


def is_reachable(
    urls: Union[str, tuple],
    timeout: Union[float, Tuple[float, float]] = 1) -> bool:
    """Check if the specified url is reachable"""

    try:
        if isinstance(urls, Tuple):
            return all(is_reachable(u) for u in urls)
        fetch(url=urls, method=HttpMethod.HEAD, timeout=timeout)
        return True
    except (ex.ConnectTimeout, ex.ReadTimeout, ex.InvalidURL) as err:
        print(err)
        return False
    except (ex.HTTPError, ex.ConnectionError):
        return True
