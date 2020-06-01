from enum import Enum


class HttpMethod(Enum):
    OPTIONS = 'options'
    HEAD = 'head'
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'
