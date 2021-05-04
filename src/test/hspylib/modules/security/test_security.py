#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.test.hspylib.modules.security
      @file: test_security.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys
import unittest

from hspylib.core.tools.commons import safe_del_file
from hspylib.modules.security.security import encode, encrypt, decrypt, decode

PASSPHRASE = '12345'
SALT = '1234567890'

SAMPLE_IN_FILE_NAME = "resources/secret.in"
SAMPLE_OUT_FILE_NAME = "resources/secret.out"

OUT_FILE = "resources/outfile.out"
OUT_FILE_GPG = "resources/outfile.out.gpg"

ORIGINAL_FILE_CONTENTS = "HomeSetup Secrets"
ENCODED_FILE_CONTENTS = "SG9tZVNldHVwIFNlY3JldHM="


class TestSecurity(unittest.TestCase):

    # Setup tests
    def setUp(self):
        with open(SAMPLE_IN_FILE_NAME, 'w') as f_out:
            f_out.write(ORIGINAL_FILE_CONTENTS)
        with open(SAMPLE_OUT_FILE_NAME, 'w') as f_out:
            f_out.write(ENCODED_FILE_CONTENTS)
        with open(SAMPLE_IN_FILE_NAME) as f_in:
            contents = str(f_in.read().strip())
            self.assertEqual(ORIGINAL_FILE_CONTENTS, contents)
        with open(SAMPLE_OUT_FILE_NAME) as f_in:
            contents = str(f_in.read().strip())
            self.assertEqual(ENCODED_FILE_CONTENTS, contents)

    # Teardown tests
    def tearDown(self):
        safe_del_file(OUT_FILE)
        safe_del_file(OUT_FILE_GPG)

    # TEST CASES ----------

    # TC1 - Test encoding a file.
    def test_should_encode_file(self):
        encode(SAMPLE_IN_FILE_NAME, OUT_FILE)
        with open(OUT_FILE) as f_out:
            contents = str(f_out.read().strip())
            self.assertEqual(ENCODED_FILE_CONTENTS, contents)

    # TC2 - Test decoding a file.
    def test_should_decode_file(self):
        decode(SAMPLE_OUT_FILE_NAME, OUT_FILE)
        with open(OUT_FILE) as f_out:
            contents = str(f_out.read().strip())
            self.assertEqual(ORIGINAL_FILE_CONTENTS, contents)

    # TC3 - Test encrypting a file.
    def test_should_encrypt_decrypt_file(self):
        encrypt(SAMPLE_IN_FILE_NAME, OUT_FILE_GPG, PASSPHRASE, SALT)
        decrypt(OUT_FILE_GPG, OUT_FILE, PASSPHRASE, SALT)
        with open(OUT_FILE) as f_out:
            contents = str(f_out.read().strip())
            self.assertEqual(ORIGINAL_FILE_CONTENTS, contents)


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSecurity)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
