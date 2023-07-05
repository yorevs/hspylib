#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.security
      @file: security.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from hspylib.core.enums.charset import Charset
from hspylib.core.preconditions import check_argument, check_state

import base64
import os

# fmt: off
# !!!Please do not modify the values below!!!
DEFAULT_HS_SALT: str        = "HsPyLib"
DEFAULT_HS_LENGTH: int      = 32
DEFAULT_HS_ITERATIONS: int  = 100000
# fmt: on


def encode_file(in_file: str, out_file: str, binary: bool = False, encoding: str | Charset = Charset.UTF_8) -> int:
    """Encode file into base64
    :param in_file: The file to be encoded
    :param out_file: The resulting encoded file
    :param binary: The file mode text/binary
    :param encoding: The text encoding
    """
    if binary:
        with open(in_file, "rb") as f_in_file:
            with open(out_file, "wb") as f_out_file:
                data = base64.b64encode(f_in_file.read())
                return f_out_file.write(data)

    with open(in_file, "r", encoding=Charset.UTF_8.val) as f_in_file:
        with open(out_file, "w", encoding=str(encoding)) as f_out_file:
            data = base64.b64encode(str.encode(f_in_file.read()))
            return f_out_file.write(str(data, encoding=str(encoding)))


def decode_file(in_file: str, out_file: str, binary: bool = False, encoding: str | Charset = Charset.UTF_8) -> int:
    """Decode file from base64
    :param in_file: The file to be decoded
    :param out_file: The resulting decoded file
    :param binary: The file mode text/binary
    :param encoding: The text encoding
    """
    if binary:
        with open(in_file, "rb") as f_in_file:
            with open(out_file, "wb") as f_out_file:
                data = base64.b64decode(f_in_file.read())
                return f_out_file.write(data)

    with open(in_file, "r", encoding=str(encoding)) as f_in_file:
        with open(out_file, "w", encoding=str(encoding)) as f_out_file:
            data = base64.b64decode(f_in_file.read())
            return f_out_file.write(str(data, encoding=str(encoding)))


def encrypt_file(
    in_file: str,
    out_file: str,
    pass_phrase: str,
    salt: str = DEFAULT_HS_SALT,
    digest_algo: hashes.HashAlgorithm = hashes.SHA256(),
    length: int = DEFAULT_HS_LENGTH,
    iterations: int = DEFAULT_HS_ITERATIONS,
    encoding: str | Charset = Charset.UTF_8,
) -> None:
    """Encrypt file using Fernet cryptography
    :param in_file: The file to be encrypted
    :param out_file: The resulting encrypted file
    :param pass_phrase: The passphrase to encrypt the file
    :param salt: A random data that is used as an additional input to a one-way function to hash data.
    :param digest_algo: The digest encrypting algorithm
    :param length: The desired length of the derived key in bytes. Maximum is (232 - 1) * algorithm.digest_size.
    :param iterations: The number of iterations to perform of the hash function.
    :param encoding: The name of the encoding used to decode or encode the file.
    """

    kdf = PBKDF2HMAC(
        algorithm=digest_algo,
        length=length,
        salt=salt.encode(str(encoding)),
        iterations=iterations,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(pass_phrase.encode(str(encoding))))
    f = Fernet(key)
    check_argument(os.path.exists(in_file), 'Input file "{}" does not exist', in_file)
    with open(in_file, encoding=str(encoding)) as f_in_file:
        with open(out_file, "w", encoding=str(encoding)) as f_out_file:
            f_out_file.write(f.encrypt(f_in_file.read().encode(str(encoding))).decode(str(encoding)))
    check_state(os.path.exists(out_file), 'Unable to encrypt file "{}"', in_file)


def decrypt_file(
    in_file: str,
    out_file: str,
    pass_phrase: str,
    salt: str = DEFAULT_HS_SALT,
    digest_algo: hashes.HashAlgorithm = hashes.SHA256(),
    length: int = DEFAULT_HS_LENGTH,
    iterations: int = DEFAULT_HS_ITERATIONS,
    encoding: str | Charset = Charset.UTF_8,
) -> None:
    """Decrypt file using Fernet cryptography
    :param in_file: The file to be decrypted
    :param out_file: The resulting decrypted file
    :param pass_phrase: The passphrase to decrypt the file
    :param salt: A random data that is used as an additional input to a one-way function to hash data.DO
    :param digest_algo: The digest decrypting algorithm
    :param length: The desired length of the derived key in bytes. Maximum is (232 - 1) * algorithm.digest_size.
    :param iterations: The number of iterations to perform of the hash function.
    :param encoding: The name of the encoding used to decode or encode the file.
    """

    kdf = PBKDF2HMAC(
        algorithm=digest_algo,
        length=length,
        salt=salt.encode(str(encoding)),
        iterations=iterations,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(pass_phrase.encode(str(encoding))))
    f = Fernet(key)
    check_argument(os.path.exists(in_file), 'Input file "{}" does not exist', in_file)
    with open(in_file, encoding=str(encoding)) as f_in_file:
        with open(out_file, "w", encoding=str(encoding)) as f_out_file:
            f_out_file.write(f.decrypt(f_in_file.read().encode(str(encoding))).decode(str(encoding)))
    check_state(os.path.exists(out_file), 'Unable to decrypt file "{}"', in_file)


def b64_encode(text: str, encoding: str | Charset = Charset.UTF_8) -> str:
    """Encode a text using Base64.
    :param text The text to be encoded
    :param encoding The name of the encoding used to decode or encode the text.
    """

    return str(base64.b64encode(bytes(text, str(encoding))), str(encoding))


def b64_decode(text: str, encoding: str | Charset = Charset.UTF_8) -> str:
    """Decode a Base64 encoded text.
    :param text The text to be decoded
    :param encoding The name of the encoding used to decode or encode the text.
    """
    return str(base64.b64decode(bytes(text, str(encoding))), str(encoding))
