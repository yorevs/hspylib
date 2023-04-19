#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.enums
      @file: content_type.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from hspylib.core.enums.charset import Charset
from hspylib.core.enums.enumeration import Enumeration
from typing import Tuple


class ContentType(Enumeration):
    """Enumeration to wrap all http content types. The 'Content-Type' representation header is used to indicate the
    original media type of the resource (prior to any content encoding applied for sending)."""

    # fmt: off

    APPLICATION_ATOM_XML                = 'application/atom+xml'
    APPLICATION_ECMASCRIPT              = 'application/ecmascript'
    APPLICATION_JSON                    = 'application/json'
    APPLICATION_VNP_API_JSON            = 'application/vpn.api+json'
    APPLICATION_JAVASCRIPT              = 'application/javascript'
    APPLICATION_OCTET_STREAM            = 'application/octet-stream'
    APPLICATION_OGG                     = 'application/ogg'
    APPLICATION_PDF                     = 'application/pdf'
    APPLICATION_POSTSCRIPT              = 'application/postscript'
    APPLICATION_RDF_XML                 = 'application/rdf+xml'
    APPLICATION_RSS_XML                 = 'application/rss+xml'
    APPLICATION_SOAP_XML                = 'application/soap+xml'
    APPLICATION_FONT_WOFF               = 'application/font-woff'
    APPLICATION_X_YAML                  = 'application/x-yaml'
    APPLICATION_XHTML_XML               = 'application/xhtml+xml'
    APPLICATION_XML                     = 'application/xml'
    APPLICATION_DTD                     = 'application/xml-dtd'
    APPLICATION_XOP_XML                 = 'application/xop+xml'
    APPLICATION_ZIP                     = 'application/zip'
    APPLICATION_GZIP                    = 'application/gzip'
    APPLICATION_GRAPHQL                 = 'application/graphql'
    APPLICATION_X_WWW_FORM_URLENCODED   = 'application/x-www-form-urlencoded'
    AUDIO_BASIC                         = 'audio/basic'
    AUDIO_L24                           = 'audio/L24'
    AUDIO_MP4                           = 'audio/mp4'
    AUDIO_MPEG                          = 'audio/mpeg'
    AUDIO_OGG                           = 'audio/ogg'
    AUDIO_VORBIX                        = 'audio/vorbis'
    AUDIO_VND_RN_REALAUDIO              = 'audio/vnd.rn-realaudio'
    AUDIO_VND_WAVE                      = 'audio/vnd.wave'
    AUDIO_WEBM                          = 'audio/webm'
    IMAGE_GIF                           = 'image/gif'
    IMAGE_JPEG                          = 'image/jpeg'
    IMAGE_PJPEG                         = 'image/pjpeg'
    IMAGE_PNG                           = 'image/png'
    IMAGE_SVG_XML                       = 'image/svg+xml'
    IMAGE_TIFF                          = 'image/tiff'
    MESSAGE_HTTP                        = 'prompt_msg/http'
    MESSAGE_IMDN_XML                    = 'prompt_msg/imdn+xml'
    MESSAGE_PARTIAL                     = 'prompt_msg/partial'
    MESSAGE_RFC_822                     = 'prompt_msg/rfc822'
    MULTIPART_MIXED                     = 'multipart/mixed'
    MULTIPART_ALTERNATIVE               = 'multipart/alternative'
    MULTIPART_RELATED                   = 'multipart/related'
    MULTIPART_FORM_DATA                 = 'multipart/form-data'
    MULTIPART_SIGNED                    = 'multipart/signed'
    MULTIPART_ENCRYPTED                 = 'multipart/encrypted'
    TEXT_CMD                            = 'text/cmd'
    TEXT_CSS                            = 'text/css'
    TEXT_CSV                            = 'text/cvs'
    TEXT_HTML                           = 'text/html'
    TEXT_PLAIN                          = 'text/plain'
    TEXT_VCARD                          = 'text/vcard'
    TEXT_XML                            = 'text/xml'

    # fmt: on

    def as_header(self, encoding: Charset = Charset.UTF_8) -> Tuple[str, str]:
        """Return this content type as an http header."""
        return "Content-Type", f"{self.value}; charset={str(encoding)}"

    @property
    def val(self) -> str:
        return str(self.value)
