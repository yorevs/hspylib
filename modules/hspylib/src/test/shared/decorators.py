#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.shared
      @file: decorators.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import os
import unittest

from hspylib.core.tools.commons import str_to_bool

it_disabled = str_to_bool(os.environ.get('HSPYLIB_IT_DISABLED', 'True'))

integration_test = unittest.skipIf(
    it_disabled,
    f'Disabled = {it_disabled} :integration tests because it needs docker container running'
)
