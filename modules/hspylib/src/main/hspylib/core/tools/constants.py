#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   Commonly used regex expressions

   @project: HSPyLib
   @package: main.tools
      @file: constants.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

# Commonly used constants

TRUE_VALUES = ['true', 'on', 'yes', '1', 'y']

# Regex expressions

RE_UUID = r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'

RE_PHONE_NUMBER = r'((\\d{2})?\\s)?(\\d{4,5}\\-\\d{4})'

RE_COMMON_2_30_NAME = r'[a-zA-Z]\\w{2,30}'

RE_EMAIL_W3C = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$'

RE_SIMPLE_URL = r'^(?:http(s)?:\\/\\/)?[\\w.-]+(?:\\.[\\w\\.-]+)+[\\w\\-\\._~:/?#[\\]@!\\$&\'\\(\\)\\*\\+,;=.]+$'

RE_VERSION_STRING = r'([0-9]+\.){2}[0-9]+((\-(DEVELOPMENT|SNAPSHOT|STABLE|RELEASE))?)$'

RE_IP_V4 = r'((2((5[0-5])|[0-4][0-9])|(1([0-9]{2}))|(0|([1-9][0-9]))|([0-9]))\.){3}(2((5[0-5])|' \
           r'[0-4][0-9])|(1([0-9]{2}))|(0|([1-9][0-9]))|([0-9]))'

# Date and time formats

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

DATE_FORMAT = "%Y-%m-%d"

TIME_FORMAT = "%H:%M:%S"
