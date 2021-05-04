#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.mock
      @file: mock_server_handler.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
from http.server import BaseHTTPRequestHandler
from typing import Tuple

from requests.structures import CaseInsensitiveDict

from hspylib.core.enum.content_type import ContentType
from hspylib.core.enum.http_code import HttpCode
from hspylib.core.enum.http_method import HttpMethod


class MockServerHandler(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: Tuple[str, int], parent):
        self.parent = parent
        super().__init__(request, client_address, parent)

    @staticmethod
    def remove_reserved_headers(headers: CaseInsensitiveDict):
        filtered = {}
        if headers:
            reserved = ['content-size', 'server', 'date']
            for header in headers:
                if header.lower() not in reserved:
                    filtered[header] = headers[header]
        return filtered

    def process_headers(self,
                        headers: CaseInsensitiveDict = None,
                        content_type: ContentType = ContentType.APPLICATION_JSON,
                        content_length: int = 0):
        headers = MockServerHandler.remove_reserved_headers(headers)
        if headers and len(headers) > 0:
            for key, value in headers.items():
                self.send_header(key, value)
        self.send_header("Server", 'MockServer v{}'.format(self.parent.version))
        self.send_header("Date", self.date_time_string())
        self.send_header("Content-Type", str(content_type))
        self.send_header("Content-Length", str(content_length))
        self.end_headers()

    def process_default(self,
                        code: HttpCode = HttpCode.OK,
                        content_type: ContentType = ContentType.APPLICATION_JSON,
                        headers: CaseInsensitiveDict = None):
        log.debug('Processing a default request status_code={} content-type={}'.format(code, content_type))
        self.send_response_only(code.value)
        self.process_headers(headers, content_type)

    def process_request(self, method: HttpMethod):
        if self.parent.is_allowed(method):
            request = self.parent.mock(method, self.path)
            if request:
                log.debug('Processing a request status_code={} content-type={}'.format(
                    request.status_code, request.content_type))
                if not request.status_code:
                    code = HttpCode.INTERNAL_SERVER_ERROR.value
                    request.body = 'Mocked response status_code must be provided'
                elif method in ['OPTIONS', 'HEAD']:
                    code = request.status_code.value
                    request.body = None
                else:
                    code = request.status_code.value
                headers = request.headers if request.headers else []
                self.send_response_only(code)
                if request.received_body and 'Content-Length' in self.headers:
                    length = int(self.headers['Content-Length'])
                    request.body = self.rfile.read(length).decode(str(request.encoding))
                    self.process_headers(headers, request.content_type, length)
                else:
                    self.process_headers(headers, request.content_type, len(request.body) if request.body else 0)
                if request.body:
                    self.wfile.write(request.body.encode(str(request.encoding)))
            else:
                self.process_default(HttpCode.NOT_FOUND)
        else:
            self.process_default(HttpCode.METHOD_NOT_ALLOWED)

    def find_allowed_methods(self):
        allowed_methods = ['OPTIONS']
        if self.parent.is_allowed(HttpMethod.HEAD):
            allowed_methods.append('HEAD')
        if self.parent.is_allowed(HttpMethod.GET):
            allowed_methods.append('GET')
        if self.parent.is_allowed(HttpMethod.POST):
            allowed_methods.append('POST')
        if self.parent.is_allowed(HttpMethod.PUT):
            allowed_methods.append('PUT')
        if self.parent.is_allowed(HttpMethod.PATCH):
            allowed_methods.append('PATCH')
        if self.parent.is_allowed(HttpMethod.DELETE):
            allowed_methods.append('DELETE')
        return allowed_methods

    def do_OPTIONS(self):
        mock_request = self.parent.mock(HttpMethod.OPTIONS, self.path)
        headers = CaseInsensitiveDict({'Allow': ', '.join(self.find_allowed_methods())})
        if mock_request:
            self.process_request(mock_request)
        else:
            self.process_default(HttpCode.NO_CONTENT, headers=headers)

    def do_HEAD(self):
        self.process_request(HttpMethod.HEAD)

    def do_GET(self):
        self.process_request(HttpMethod.GET)

    def do_POST(self):
        self.process_request(HttpMethod.POST)

    def do_PUT(self):
        self.process_request(HttpMethod.PUT)

    def do_PATCH(self):
        self.process_request(HttpMethod.PATCH)

    def do_DELETE(self):
        self.process_request(HttpMethod.DELETE)
