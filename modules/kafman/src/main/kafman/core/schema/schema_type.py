#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: schema_type.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration


class SchemaType(Enumeration):
    """TODO"""

    # fmt: off
    PLAIN           = 'PLAIN'
    AVRO            = 'AVRO'
    JSON            = 'JSON'
    PROTOBUF        = 'PROTOBUF'
    # fmt: on
