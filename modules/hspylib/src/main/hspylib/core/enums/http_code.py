#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.enums
      @file: http_code.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.preconditions import check_not_none
from hspylib.modules.cli.vt100.vt_color import VtColor


class HttpCode(Enumeration):
    """HTTP status code constants defined by the proposed HTTP/1.1 specification at http://www.ietf.org/rfc/rfc2068.txt.
    Ref:. http://www.cs.ait.ac.th/~on/O/oreilly/java-ent/servlet/appc_01.htm
    """

    # fmt: off

    # 1xx Informational Codes
    CONTINUE                            = 100, 'Continue'
    SWITCHING_PROTOCOLS                 = 101, 'Switching Protocols'
    PROCESSING                          = 102, 'Processing'
    EARLY_HINTS                         = 103, 'Early Hints'

    # 2xx Success Codes
    OK                                  = 200, 'OK'
    CREATED                             = 201, 'Created'
    ACCEPTED                            = 202, 'Accepted'
    NON_AUTHORITATIVE_INFORMATION       = 203, 'Non-Authoritative Information'
    NO_CONTENT                          = 204, 'No Content'
    RESET_CONTENT                       = 205, 'Reset Content'
    PARTIAL_CONTENT                     = 206, 'Partial Content'
    MULTI_STATUS                        = 207, 'Multi-Status'
    ALREADY_REPORTED                    = 208, 'Already Reported'
    IM_USED                             = 226, 'IM Used'

    # 3xx Redirection Codes
    MULTIPLE_CHOICES                    = 300, 'Multiple Choices'
    MOVED_PERMANENTLY                   = 301, 'Moved Permanently'
    FOUND                               = 302, 'Found'
    SEE_OTHER                           = 303, 'See Other'
    NOT_MODIFIED                        = 304, 'Not Modified'
    USE_PROXY                           = 305, 'Use Proxy'
    TEMPORARY_REDIRECT                  = 307, 'Temporary Redirect'
    PERMANENT_REDIRECT                  = 308, 'Permanent Redirect'

    # 4xx Client Error Codes
    BAD_REQUEST                         = 400, 'Bad Request'
    UNAUTHORIZED                        = 401, 'Unauthorized'
    PAYMENT_REQUIRED                    = 402, 'Payment Required'
    FORBIDDEN                           = 403, 'Forbidden'
    NOT_FOUND                           = 404, 'Not Found'
    METHOD_NOT_ALLOWED                  = 405, 'Method Not Allowed'
    NOT_ACCEPTABLE                      = 406, 'Not Acceptable'
    PROXY_AUTHENTICATION_REQUIRED       = 407, 'Proxy Authentication Required'
    REQUEST_TIMEOUT                     = 408, 'Request Timeout'
    CONFLICT                            = 409, 'Conflict'
    GONE                                = 410, 'Gone'
    LENGTH_REQUIRED                     = 411, 'Length Required'
    PRECONDITION_FAILED                 = 412, 'Precondition Failed'
    PAYLOAD_TOO_LARGE                   = 413, 'Payload Too Large'
    REQUEST_URI_TOO_LONG                = 414, 'Request-URI Too Long'
    UNSUPPORTED_MEDIA_TYPE              = 415, 'Unsupported Media Type'
    REQUESTED_RANGE_NOT_SATISFIABLE     = 416, 'Requested Range Not Satisfiable'
    EXPECTATION_FAILED                  = 417, 'Expectation Failed'
    MISDIRECTED_REQUEST                 = 421, 'Misdirected Request'
    UNPROCESSABLE_ENTITY                = 422, 'Unprocessable Entity'
    LOCKED                              = 423, 'Locked'
    FAILED_DEPENDENCY                   = 424, 'Failed Dependency'
    TOO_EARLY                           = 425, 'Too Early'
    UPGRADE_REQUIRED                    = 426, 'Upgrade Required'
    PRECONDITION_REQUIRED               = 428, 'Precondition Required'
    TOO_MANY_REQUESTS                   = 429, 'Too Many Requests'
    REQUEST_HEADER_FIELDS_TOO_LARGE     = 431, 'Request Header Fields Too Large'
    CONNECTION_CLOSED_WITHOUT_RESPONSE  = 444, 'Connection Closed Without Response'
    UNAVAILABLE_FOR_LEGAL_REASONS       = 451, 'Unavailable For Legal Reasons'
    CLIENT_CLOSED_REQUEST               = 499, 'Client Closed Request'

    # 5xx Server Error
    INTERNAL_SERVER_ERROR               = 500, 'Internal Server Error'
    NOT_IMPLEMENTED                     = 501, 'Not Implemented'
    BAD_GATEWAY                         = 502, 'Bad Gateway'
    SERVICE_UNAVAILABLE                 = 503, 'Service Unavailable'
    GATEWAY_TIMEOUT                     = 504, 'Gateway Timeout'
    HTTP_VERSION_NOT_SUPPORTED          = 505, 'HTTP Version Not Supported'
    VARIANT_ALSO_NEGOTIATES             = 506, 'Variant Also Negotiates'
    INSUFFICIENT_STORAGE                = 507, 'Insufficient Storage'
    LOOP_DETECTED                       = 508, 'Loop Detected'
    NOT_EXTENDED                        = 510, 'Not Extended'
    NETWORK_AUTHENTICATION_REQUIRED     = 511, 'Network Authentication Required'
    NETWORK_CONNECT_TIMEOUT_ERROR       = 599, 'Network Connect Timeout Error'

    # fmt: on

    @classmethod
    def of(cls, status_code: int) -> "HttpCode":
        found = next(filter(lambda en: en.code == status_code, list(cls)), None)
        return check_not_none(found, '"{}" code does not correspond to a valid "HttpCode"', status_code)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        if self.is_2xx():
            color = VtColor.GREEN.code
        elif self.is_3xx():
            color = VtColor.YELLOW.code
        elif self.is_4xx() or self.is_5xx():
            color = VtColor.RED.code
        else:
            color = VtColor.WHITE.code

        return f"{color}({self.code}) {self.reason}{VtColor.NC.code}"

    @property
    def code(self) -> int:
        return self.value[0]

    @property
    def reason(self) -> str:
        return self.value[1]

    def is_1xx(self) -> bool:
        return 100 <= self.code < 200

    def is_2xx(self) -> bool:
        return 200 <= self.code < 300

    def is_3xx(self) -> bool:
        return 300 <= self.code < 400

    def is_4xx(self) -> bool:
        return 400 <= self.code < 500

    def is_5xx(self) -> bool:
        return 500 <= self.code < 600
