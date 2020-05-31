import json
import subprocess

# @purpose: TODO
from main.hspylib.tools.commons import sysout, syserr


def __convert_headers(headers: dict):
    flat_headers = {}
    for d in headers:
        flat_headers.update(d)
    str_headers = ""
    for key, value in flat_headers.items():
        temp = "{}={}".format(key, value)
        str_headers += temp if not str_headers else "," + temp

    return '"{}"'.format(str_headers)


# @purpose: TODO
def __convert_body(body):
    if type(body) is str:
        return body
    elif type(body) is dict:
        return json.dumps(body)
    else:
        return json.dumps(body.__dict__)


# @purpose: TODO
def fetch(url, method='GET', headers=None, body=None, silent=True):
    response = None
    cmd_args = ['fetch.bash', method, '--silent']
    if headers is not None:
        cmd_args.append('--headers')
        cmd_args.append(__convert_headers(headers))
    if body is not None:
        cmd_args.append('--body')
        cmd_args.append(__convert_body(body))
    cmd_args.append(url)

    try:
        if not silent:
            sysout('Fetching: method={} headers={} body={} url={} ...'.format(
                method, headers if headers else '[]', body if body else '{}', url))
        response = subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)
        return json.dumps(response).strip()
    except subprocess.CalledProcessError as err:
        syserr("Failed to fetch: method={} headers={} body={} url={} \t => {}"
               .format(method, headers if headers else '[]', body if body else '', url, err))
    except TypeError:
        # If this happen, is because the response is not json format
        pass

    return response


# @purpose: TODO
def get(url, headers=None, silent=False):
    return fetch(url, headers=headers, silent=silent)


# @purpose: TODO
def delete(url, headers=None, silent=False):
    return fetch(url, 'DELETE', headers, silent)


# @purpose: TODO
def post(url, body, headers=None, silent=False):
    return fetch(url, 'POST', headers, body, silent)


# @purpose: TODO
def put(url, body, headers=None, silent=False):
    return fetch(url, 'PUT', headers, body, silent)


# @purpose: TODO
def patch(url, body, headers=None, silent=False):
    return fetch(url, 'PATCH', headers, body, silent)
