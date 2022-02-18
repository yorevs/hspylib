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

   Copyright 2021, HSPyLib team
"""

from http import HTTPStatus as http_code

from hspylib.core.enums.enumeration import Enumeration


class HttpCode(Enumeration):
    """TODO"""

    # @formatter:off

    # 1xx Informational Codes
    CONTINUE                            = http_code.CONTINUE
    SWITCHING_PROTOCOLS                 = http_code.SWITCHING_PROTOCOLS
    PROCESSING                          = http_code.PROCESSING
    EARLY_HINTS                         = http_code.EARLY_HINTS

    # 2xx Success Codes
    OK                                  = http_code.OK
    CREATED                             = http_code.CREATED
    ACCEPTED                            = http_code.ACCEPTED
    NON_AUTHORITATIVE_INFORMATION       = http_code.NON_AUTHORITATIVE_INFORMATION
    NO_CONTENT                          = http_code.NO_CONTENT
    RESET_CONTENT                       = http_code.RESET_CONTENT
    PARTIAL_CONTENT                     = http_code.PARTIAL_CONTENT
    MULTI_STATUS                        = http_code.MULTI_STATUS
    ALREADY_REPORTED                    = http_code.ALREADY_REPORTED
    IM_USED                             = http_code.IM_USED

    # 3xx Redirection Codes
    MULTIPLE_CHOICES                    = http_code.MULTIPLE_CHOICES
    MOVED_PERMANENTLY                   = http_code.MOVED_PERMANENTLY
    FOUND                               = http_code.FOUND
    SEE_OTHER                           = http_code.SEE_OTHER
    NOT_MODIFIED                        = http_code.NOT_MODIFIED
    USE_PROXY                           = http_code.USE_PROXY
    TEMPORARY_REDIRECT                  = http_code.TEMPORARY_REDIRECT
    PERMANENT_REDIRECT                  = http_code.PERMANENT_REDIRECT

    # 4xx Client Error Codes
    BAD_REQUEST                         = http_code.BAD_REQUEST
    UNAUTHORIZED                        = http_code.UNAUTHORIZED
    PAYMENT_REQUIRED                    = http_code.PAYMENT_REQUIRED
    FORBIDDEN                           = http_code.FORBIDDEN
    NOT_FOUND                           = http_code.NOT_FOUND
    METHOD_NOT_ALLOWED                  = http_code.METHOD_NOT_ALLOWED
    NOT_ACCEPTABLE                      = http_code.NOT_ACCEPTABLE
    PROXY_AUTHENTICATION_REQUIRED       = http_code.PROXY_AUTHENTICATION_REQUIRED
    REQUEST_TIMEOUT                     = http_code.REQUEST_TIMEOUT
    CONFLICT                            = http_code.CONFLICT
    GONE                                = http_code.GONE
    LENGTH_REQUIRED                     = http_code.LENGTH_REQUIRED
    PRECONDITION_FAILED                 = http_code.PRECONDITION_FAILED
    PAYLOAD_TOO_LARGE                   = 413
    REQUEST_URI_TOO_LONG                = http_code.REQUEST_URI_TOO_LONG
    UNSUPPORTED_MEDIA_TYPE              = http_code.UNSUPPORTED_MEDIA_TYPE
    REQUESTED_RANGE_NOT_SATISFIABLE     = http_code.REQUESTED_RANGE_NOT_SATISFIABLE
    EXPECTATION_FAILED                  = http_code.EXPECTATION_FAILED
    UNPROCESSABLE_ENTITY                = http_code.UNPROCESSABLE_ENTITY
    LOCKED                              = http_code.LOCKED
    FAILED_DEPENDENCY                   = http_code.FAILED_DEPENDENCY
    UPGRADE_REQUIRED                    = http_code.UPGRADE_REQUIRED
    PRECONDITION_REQUIRED               = http_code.PRECONDITION_REQUIRED
    TOO_MANY_REQUESTS                   = http_code.TOO_MANY_REQUESTS
    REQUEST_HEADER_FIELDS_TOO_LARGE     = http_code.REQUEST_HEADER_FIELDS_TOO_LARGE
    CONNECTION_CLOSED_WITHOUT_RESPONSE  = 444
    UNAVAILABLE_FOR_LEGAL_REASONS       = 451
    CLIENT_CLOSED_REQUEST               = 499

    # 5xx Server Error
    INTERNAL_SERVER_ERROR               = http_code.INTERNAL_SERVER_ERROR
    NOT_IMPLEMENTED                     = http_code.NOT_IMPLEMENTED
    BAD_GATEWAY                         = http_code.BAD_GATEWAY
    SERVICE_UNAVAILABLE                 = http_code.SERVICE_UNAVAILABLE
    GATEWAY_TIMEOUT                     = http_code.GATEWAY_TIMEOUT
    HTTP_VERSION_NOT_SUPPORTED          = http_code.HTTP_VERSION_NOT_SUPPORTED
    VARIANT_ALSO_NEGOTIATES             = http_code.VARIANT_ALSO_NEGOTIATES
    INSUFFICIENT_STORAGE                = http_code.INSUFFICIENT_STORAGE
    LOOP_DETECTED                       = http_code.LOOP_DETECTED
    NOT_EXTENDED                        = http_code.NOT_EXTENDED
    NETWORK_AUTHENTICATION_REQUIRED     = http_code.NETWORK_AUTHENTICATION_REQUIRED
    NETWORK_CONNECT_TIMEOUT_ERROR       = 599

    # @formatter:on
