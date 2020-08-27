from enum import Enum


class HttpMethod(Enum):
    OPTIONS = 'menu_options'
    HEAD = 'head'
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'
