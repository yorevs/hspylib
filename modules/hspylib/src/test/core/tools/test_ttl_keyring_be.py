#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.tools
      @file: test_text_tools.py
   @created: Thu, 07 Jul 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import sys
import unittest
from time import sleep

import keyring

from hspylib.core.tools.ttl_keyring_be import TTLKeyringBE
from hspylib.core.tools.zoned_datetime import now_ms


class TestTextTools(unittest.TestCase):

    def test_should_expire_the_passwords_on_the_right_timestamp(self):
        m, s = 0, 3
        t = m * 60 + s
        now = now_ms()
        be = TTLKeyringBE(m, s)
        keyring.set_keyring(be)
        self.assertIsNone(keyring.get_password('test-srv', 'test-un'), 'Password SHOULD be None')
        keyring.set_password('test-srv', 'test-un', 'test-pwd')
        self.assertIsNotNone(keyring.get_password('test-srv', 'test-un'), 'Password SHOULD NOT be None')
        sleep(t - 1)
        self.assertIsNotNone(keyring.get_password('test-srv', 'test-un'), 'Password SHOULD NOT be None')
        sleep(2)
        self.assertIsNone(keyring.get_password('test-srv', 'test-un'), 'Password SHOULD have expired')
        done = now_ms()
        self.assertEqual(now + t + 1, done, 'Time elapsed should be almost equal')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTextTools)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
