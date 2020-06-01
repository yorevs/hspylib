from enum import Enum


class HttpMethod(Enum):
    HEAD = 'head'
    OPTIONS = 'options'
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'
