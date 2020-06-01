from enum import Enum


class HttpMethod(Enum):
    HEAD = 'head'
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'
    OPTIONS = 'options'
