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
from hspylib.core.zoned_datetime import now_ms
from hspylib.modules.cache.ttl_keyring_be import TTLKeyringBE


class TestTextTools(unittest.TestCase):

    TEST_SERVICE = 'test-srv'
    TEST_USER = 'test-un'

    def setUp(self) -> None:
        self.m, self.s = 0, 3
        keyring.set_keyring(TTLKeyringBE(self.m, self.s))
        keyring.delete_password(self.TEST_SERVICE, self.TEST_USER)

    def test_should_expire_the_passwords_on_the_right_timestamp(self) -> None:
        now = now_ms()
        t = self.m * 60 + self.s
        self.assertIsNone(keyring.get_password(self.TEST_SERVICE, self.TEST_USER), 'Password SHOULD be None')
        keyring.set_password(self.TEST_SERVICE, self.TEST_USER, 'test-pwd')
        self.assertIsNotNone(keyring.get_password(self.TEST_SERVICE, self.TEST_USER), 'Password SHOULD NOT be None')
        sleep(t - 1)
        self.assertIsNotNone(keyring.get_password(self.TEST_SERVICE, self.TEST_USER), 'Password SHOULD NOT be None')
        sleep(2)
        done = now_ms()
        expected = 1 + now + t
        self.assertIsNone(keyring.get_password(self.TEST_SERVICE, self.TEST_USER), 'Password SHOULD have expired')
        self.assertEqual(expected, done, 'Time elapsed SHOULD be equal')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTextTools)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
