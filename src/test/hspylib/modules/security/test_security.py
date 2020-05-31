import os
import unittest

from main.hspylib.modules.security.security import encode, encrypt, decrypt, decode

PASSPHRASE = '12345'

SAMPLE_IN_FILE_NAME = "resources/secret.in"
SAMPLE_OUT_FILE_NAME = "resources/secret.out"

OUT_FILE = "resources/outfile.out"
OUT_FILE_GPG = "resources/outfile.out.gpg"

ORIGINAL_FILE_CONTENTS = "HomeSetup Secrets"
ENCODED_FILE_CONTENTS = "SG9tZVNldHVwIFNlY3JldHM="


class TestHhsLib(unittest.TestCase):

    # Setup tests
    def setUp(self):
        with open(SAMPLE_IN_FILE_NAME, 'w') as f_in:
            f_in.write(ORIGINAL_FILE_CONTENTS)
        with open(SAMPLE_OUT_FILE_NAME, 'w') as f_in:
            f_in.write(ENCODED_FILE_CONTENTS)
    
    # Teardown tests
    def tearDown(self):
        if os.path.exists(OUT_FILE):
            os.remove(OUT_FILE)
        if os.path.exists(OUT_FILE_GPG):
            os.remove(OUT_FILE_GPG)
    
    # TEST CASES ----------

    # TC1 - Test encoding a file.
    def test_should_encode_file(self):
        with open(SAMPLE_IN_FILE_NAME) as f_in:
            contents = str(f_in.read().strip())
            self.assertEqual(ORIGINAL_FILE_CONTENTS, contents)
        encode(SAMPLE_IN_FILE_NAME, OUT_FILE)
        with open(OUT_FILE) as f_out:
            contents = str(f_out.read().strip())
            self.assertEqual(ENCODED_FILE_CONTENTS, contents)

    # TC2 - Test decoding a file.
    def test_should_decode_file(self):
        with open(SAMPLE_OUT_FILE_NAME) as f_in:
            contents = str(f_in.read().strip())
            self.assertEqual(ENCODED_FILE_CONTENTS, contents)
        decode(SAMPLE_OUT_FILE_NAME, OUT_FILE)
        with open(OUT_FILE) as f_out:
            contents = str(f_out.read().strip())
            self.assertEqual(ORIGINAL_FILE_CONTENTS, contents)

    # TC3 - Test encrypting a file.
    def test_should_encrypt_decrypt_file(self):
        with open(SAMPLE_IN_FILE_NAME) as f_in:
            contents = str(f_in.read().strip())
            self.assertEqual(ORIGINAL_FILE_CONTENTS, contents)
        encrypt(SAMPLE_IN_FILE_NAME, OUT_FILE_GPG, PASSPHRASE)
        decrypt(OUT_FILE_GPG, OUT_FILE, PASSPHRASE)
        with open(OUT_FILE) as f_out:
            contents = str(f_out.read().strip())
            self.assertEqual(ORIGINAL_FILE_CONTENTS, contents)


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHhsLib)
    unittest.TextTestRunner(verbosity=2).run(suite)
