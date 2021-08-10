#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: hspylib.main.hspylib.core.enum
      @file: http_code.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from http import HTTPStatus as code

from hspylib.core.enums.enumeration import Enumeration


class HttpCode(Enumeration):
    """TODO"""

    # @formatter:off

    # 1xx Informational Codes
    CONTINUE                            = code.CONTINUE
    SWITCHING_PROTOCOLS                 = code.SWITCHING_PROTOCOLS
    PROCESSING                          = code.PROCESSING
    EARLY_HINTS                         = code.EARLY_HINTS

    # 2xx Success Codes
    OK                                  = code.OK
    CREATED                             = code.CREATED
    ACCEPTED                            = code.ACCEPTED
    NON_AUTHORITATIVE_INFORMATION       = code.NON_AUTHORITATIVE_INFORMATION
    NO_CONTENT                          = code.NO_CONTENT
    RESET_CONTENT                       = code.RESET_CONTENT
    PARTIAL_CONTENT                     = code.PARTIAL_CONTENT
    MULTI_STATUS                        = code.MULTI_STATUS
    ALREADY_REPORTED                    = code.ALREADY_REPORTED
    IM_USED                             = code.IM_USED

    # 3xx Redirection Codes
    MULTIPLE_CHOICES                    = code.MULTIPLE_CHOICES
    MOVED_PERMANENTLY                   = code.MOVED_PERMANENTLY
    FOUND                               = code.FOUND
    SEE_OTHER                           = code.SEE_OTHER
    NOT_MODIFIED                        = code.NOT_MODIFIED
    USE_PROXY                           = code.USE_PROXY
    TEMPORARY_REDIRECT                  = code.TEMPORARY_REDIRECT
    PERMANENT_REDIRECT                  = code.PERMANENT_REDIRECT

    # 4xx Client Error Codes
    BAD_REQUEST                         = code.BAD_REQUEST
    UNAUTHORIZED                        = code.UNAUTHORIZED
    PAYMENT_REQUIRED                    = code.PAYMENT_REQUIRED
    FORBIDDEN                           = code.FORBIDDEN
    NOT_FOUND                           = code.NOT_FOUND
    METHOD_NOT_ALLOWED                  = code.METHOD_NOT_ALLOWED
    NOT_ACCEPTABLE                      = code.NOT_ACCEPTABLE
    PROXY_AUTHENTICATION_REQUIRED       = code.PROXY_AUTHENTICATION_REQUIRED
    REQUEST_TIMEOUT                     = code.REQUEST_TIMEOUT
    CONFLICT                            = code.CONFLICT
    GONE                                = code.GONE
    LENGTH_REQUIRED                     = code.LENGTH_REQUIRED
    PRECONDITION_FAILED                 = code.PRECONDITION_FAILED
    PAYLOAD_TOO_LARGE                   = 413
    REQUEST_URI_TOO_LONG                = code.REQUEST_URI_TOO_LONG
    UNSUPPORTED_MEDIA_TYPE              = code.UNSUPPORTED_MEDIA_TYPE
    REQUESTED_RANGE_NOT_SATISFIABLE     = code.REQUESTED_RANGE_NOT_SATISFIABLE
    EXPECTATION_FAILED                  = code.EXPECTATION_FAILED
    UNPROCESSABLE_ENTITY                = code.UNPROCESSABLE_ENTITY
    LOCKED                              = code.LOCKED
    FAILED_DEPENDENCY                   = code.FAILED_DEPENDENCY
    UPGRADE_REQUIRED                    = code.UPGRADE_REQUIRED
    PRECONDITION_REQUIRED               = code.PRECONDITION_REQUIRED
    TOO_MANY_REQUESTS                   = code.TOO_MANY_REQUESTS
    REQUEST_HEADER_FIELDS_TOO_LARGE     = code.REQUEST_HEADER_FIELDS_TOO_LARGE
    CONNECTION_CLOSED_WITHOUT_RESPONSE  = 444
    UNAVAILABLE_FOR_LEGAL_REASONS       = 451
    CLIENT_CLOSED_REQUEST               = 499

    # 5xx Server Error
    INTERNAL_SERVER_ERROR               = code.INTERNAL_SERVER_ERROR
    NOT_IMPLEMENTED                     = code.NOT_IMPLEMENTED
    BAD_GATEWAY                         = code.BAD_GATEWAY
    SERVICE_UNAVAILABLE                 = code.SERVICE_UNAVAILABLE
    GATEWAY_TIMEOUT                     = code.GATEWAY_TIMEOUT
    HTTP_VERSION_NOT_SUPPORTED          = code.HTTP_VERSION_NOT_SUPPORTED
    VARIANT_ALSO_NEGOTIATES             = code.VARIANT_ALSO_NEGOTIATES
    INSUFFICIENT_STORAGE                = code.INSUFFICIENT_STORAGE
    LOOP_DETECTED                       = code.LOOP_DETECTED
    NOT_EXTENDED                        = code.NOT_EXTENDED
    NETWORK_AUTHENTICATION_REQUIRED     = code.NETWORK_AUTHENTICATION_REQUIRED
    NETWORK_CONNECT_TIMEOUT_ERROR       = 599

    # @formatter:on
