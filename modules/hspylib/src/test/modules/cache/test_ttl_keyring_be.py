#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   test.tools
      @file: test_text_tools.py
   @created: Thu, 07 Jul 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import sys
import unittest
from time import sleep

import keyring

from hspylib.core.decorator.decorators import integration_test
from hspylib.core.zoned_datetime import now_ms
from hspylib.modules.cache.ttl_keyring_be import TTLKeyringBE


@integration_test
class TestTTLKeyring(unittest.TestCase):
    TEST_SERVICE = "test-srv"
    TEST_USER = "test-un"

    def setUp(self) -> None:
        self.min, self.sec = 0, 3
        keyring.set_keyring(TTLKeyringBE(self.min, self.sec))
        keyring.delete_password(self.TEST_SERVICE, self.TEST_USER)

    def test_should_expire_the_passwords_on_the_right_timestamp(self) -> None:
        timeout = self.min * 60 + self.sec
        self.assertIsNone(keyring.get_password(self.TEST_SERVICE, self.TEST_USER), "Password SHOULD be None")
        started = now_ms()
        lower_limit = started + timeout + 1
        upper_limit = started + timeout + 2
        keyring.set_password(self.TEST_SERVICE, self.TEST_USER, "test-pwd")
        self.assertIsNotNone(keyring.get_password(self.TEST_SERVICE, self.TEST_USER), "Password SHOULD NOT be None")
        sleep(timeout - 1)
        self.assertIsNotNone(keyring.get_password(self.TEST_SERVICE, self.TEST_USER), "Password SHOULD NOT be None")
        sleep(2)  # Wait until the timer expires: timeout + 2
        ended = now_ms()
        self.assertIsNone(keyring.get_password(self.TEST_SERVICE, self.TEST_USER), "Password SHOULD have expired")
        self.assertTrue(
            lower_limit <= ended <= upper_limit, f"Time elapsed SHOULD be in range: ({lower_limit}-{upper_limit})"
        )


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTTLKeyring)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
