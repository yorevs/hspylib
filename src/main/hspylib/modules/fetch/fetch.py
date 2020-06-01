import requests

from main.hspylib.core.enum.http_method import HttpMethod
from main.hspylib.tools.commons import sysout


# @purpose: TODO
def fetch(url: str, method: HttpMethod = HttpMethod.GET, headers=None, body=None, silent=True):
    url = url if url.startswith("http[s]?:[0-9]{0,5}//") else 'http://{}'.format(url)
    if not silent:
        sysout('Fetching: method={} headers={} body={} url={} ...'.format(
            method, headers if headers else '[]', body if body else '{}', url))
    response = requests.request(url=url, method=method.name, headers=headers, data=body)
    return response


# @purpose: TODO
def get(url: str, headers=None, silent=True):
    return fetch(url, headers=headers, silent=silent)


# @purpose: TODO
def delete(url: str, headers=None, silent=True):
    return fetch(url=url, method=HttpMethod.DELETE, headers=headers, silent=silent)


# @purpose: TODO
def post(url: str, body=None, headers=None, silent=True):
    return fetch(url, HttpMethod.POST, headers, body, silent)


# @purpose: TODO
def put(url, body=None, headers=None, silent=True):
    return fetch(url=url, method=HttpMethod.PUT, headers=headers, body=body, silent=silent)


# @purpose: TODO
def patch(url, body=None, headers=None, silent=True):
    return fetch(url=url, method=HttpMethod.PATCH, headers=headers, body=body, silent=silent)
