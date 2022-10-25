#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.enum
      @file: http_code.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from http import HTTPStatus as httpCode

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.text_tools import titlecase


class HttpCode(Enumeration):
    """HTTP status code constants defined by the proposed HTTP/1.1 specification at http://www.ietf.org/rfc/rfc2068.txt.
    Ref:http://www.cs.ait.ac.th/~on/O/oreilly/java-ent/servlet/appc_01.htm
    """

    # @formatter:off

    # 1xx Informational Codes
    CONTINUE                            = httpCode.CONTINUE
    SWITCHING_PROTOCOLS                 = httpCode.SWITCHING_PROTOCOLS
    PROCESSING                          = httpCode.PROCESSING
    EARLY_HINTS                         = httpCode.EARLY_HINTS

    # 2xx Success Codes
    OK                                  = httpCode.OK
    CREATED                             = httpCode.CREATED
    ACCEPTED                            = httpCode.ACCEPTED
    NON_AUTHORITATIVE_INFORMATION       = httpCode.NON_AUTHORITATIVE_INFORMATION
    NO_CONTENT                          = httpCode.NO_CONTENT
    RESET_CONTENT                       = httpCode.RESET_CONTENT
    PARTIAL_CONTENT                     = httpCode.PARTIAL_CONTENT
    MULTI_STATUS                        = httpCode.MULTI_STATUS
    ALREADY_REPORTED                    = httpCode.ALREADY_REPORTED
    IM_USED                             = httpCode.IM_USED

    # 3xx Redirection Codes
    MULTIPLE_CHOICES                    = httpCode.MULTIPLE_CHOICES
    MOVED_PERMANENTLY                   = httpCode.MOVED_PERMANENTLY
    FOUND                               = httpCode.FOUND
    SEE_OTHER                           = httpCode.SEE_OTHER
    NOT_MODIFIED                        = httpCode.NOT_MODIFIED
    USE_PROXY                           = httpCode.USE_PROXY
    TEMPORARY_REDIRECT                  = httpCode.TEMPORARY_REDIRECT
    PERMANENT_REDIRECT                  = httpCode.PERMANENT_REDIRECT

    # 4xx Client Error Codes
    BAD_REQUEST                         = httpCode.BAD_REQUEST
    UNAUTHORIZED                        = httpCode.UNAUTHORIZED
    PAYMENT_REQUIRED                    = httpCode.PAYMENT_REQUIRED
    FORBIDDEN                           = httpCode.FORBIDDEN
    NOT_FOUND                           = httpCode.NOT_FOUND
    METHOD_NOT_ALLOWED                  = httpCode.METHOD_NOT_ALLOWED
    NOT_ACCEPTABLE                      = httpCode.NOT_ACCEPTABLE
    PROXY_AUTHENTICATION_REQUIRED       = httpCode.PROXY_AUTHENTICATION_REQUIRED
    REQUEST_TIMEOUT                     = httpCode.REQUEST_TIMEOUT
    CONFLICT                            = httpCode.CONFLICT
    GONE                                = httpCode.GONE
    LENGTH_REQUIRED                     = httpCode.LENGTH_REQUIRED
    PRECONDITION_FAILED                 = httpCode.PRECONDITION_FAILED
    PAYLOAD_TOO_LARGE                   = 413
    REQUEST_URI_TOO_LONG                = httpCode.REQUEST_URI_TOO_LONG
    UNSUPPORTED_MEDIA_TYPE              = httpCode.UNSUPPORTED_MEDIA_TYPE
    REQUESTED_RANGE_NOT_SATISFIABLE     = httpCode.REQUESTED_RANGE_NOT_SATISFIABLE
    EXPECTATION_FAILED                  = httpCode.EXPECTATION_FAILED
    UNPROCESSABLE_ENTITY                = httpCode.UNPROCESSABLE_ENTITY
    LOCKED                              = httpCode.LOCKED
    FAILED_DEPENDENCY                   = httpCode.FAILED_DEPENDENCY
    UPGRADE_REQUIRED                    = httpCode.UPGRADE_REQUIRED
    PRECONDITION_REQUIRED               = httpCode.PRECONDITION_REQUIRED
    TOO_MANY_REQUESTS                   = httpCode.TOO_MANY_REQUESTS
    REQUEST_HEADER_FIELDS_TOO_LARGE     = httpCode.REQUEST_HEADER_FIELDS_TOO_LARGE
    CONNECTION_CLOSED_WITHOUT_RESPONSE  = 444
    UNAVAILABLE_FOR_LEGAL_REASONS       = 451
    CLIENT_CLOSED_REQUEST               = 499

    # 5xx Server Error
    INTERNAL_SERVER_ERROR               = httpCode.INTERNAL_SERVER_ERROR
    NOT_IMPLEMENTED                     = httpCode.NOT_IMPLEMENTED
    BAD_GATEWAY                         = httpCode.BAD_GATEWAY
    SERVICE_UNAVAILABLE                 = httpCode.SERVICE_UNAVAILABLE
    GATEWAY_TIMEOUT                     = httpCode.GATEWAY_TIMEOUT
    HTTP_VERSION_NOT_SUPPORTED          = httpCode.HTTP_VERSION_NOT_SUPPORTED
    VARIANT_ALSO_NEGOTIATES             = httpCode.VARIANT_ALSO_NEGOTIATES
    INSUFFICIENT_STORAGE                = httpCode.INSUFFICIENT_STORAGE
    LOOP_DETECTED                       = httpCode.LOOP_DETECTED
    NOT_EXTENDED                        = httpCode.NOT_EXTENDED
    NETWORK_AUTHENTICATION_REQUIRED     = httpCode.NETWORK_AUTHENTICATION_REQUIRED
    NETWORK_CONNECT_TIMEOUT_ERROR       = 599

    # @formatter:on

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"({self.value}) {titlecase(self.name)}"

