from typing import Optional

import requests
from hspylib.core.enum.http_method import HttpMethod
from hspylib.modules.fetch.http_response import HttpResponse
from hspylib.core.tools.commons import sysout


# @purpose: Do a request specified by method and according to parameters.
def fetch(
        url: str,
        method: HttpMethod = HttpMethod.GET,
        headers=None,
        body=None,
        silent=True) -> Optional[HttpResponse]:

    url = url if url.startswith("http") else 'http://{}'.format(url)
    if not silent:
        sysout('Fetching: method={} headers={} body={} url={} ...'.format(
            method, headers if headers else '[]', body if body else '{}', url))
    response = requests.request(url=url, method=method.name, headers=headers, data=body, timeout=3)
    return HttpResponse.of(response)


# @purpose: Do HEAD request and according to parameters.
def head(url: str, headers=None, silent=True):
    return fetch(url=url, method=HttpMethod.HEAD, headers=headers, silent=silent)


# @purpose: Do GET request and according to parameters.
def get(url: str, headers=None, silent=True):
    return fetch(url=url, headers=headers, silent=silent)


# @purpose: Do DELETE request and according to parameters.
def delete(url: str, headers=None, silent=True):
    return fetch(url=url, method=HttpMethod.DELETE, headers=headers, silent=silent)


# @purpose: Do POST request and according to parameters.
def post(url: str, body=None, headers=None, silent=True):
    return fetch(url, HttpMethod.POST, headers, body, silent)


# @purpose: Do PUT request and according to parameters.
def put(url, body=None, headers=None, silent=True):
    return fetch(url=url, method=HttpMethod.PUT, headers=headers, body=body, silent=silent)


# @purpose: Do PATCH request and according to parameters.
def patch(url, body=None, headers=None, silent=True):
    return fetch(url=url, method=HttpMethod.PATCH, headers=headers, body=body, silent=silent)
