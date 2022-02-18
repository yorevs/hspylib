#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.security
      @file: security.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from hspylib.core.tools.preconditions import check_argument, check_state

# Please do not modify this

DEFAULT_HS_SALT = 'HsPyLib'


def encode(in_file, out_file, encoding: str = 'utf-8') -> int:
    """Encode file into base64
    :param in_file: The file to be encoded
    :param out_file: The resulting encoded file
    :param encoding: The text encoding
    """
    with open(in_file, 'r', encoding=encoding) as f_in_file:
        with open(out_file, 'w', encoding=encoding) as f_out_file:
            data = base64.b64encode(str.encode(f_in_file.read()))
            return f_out_file.write(str(data, encoding=encoding))


def decode(in_file, out_file, encoding: str = 'utf-8') -> int:
    """Decode file from base64
    :param in_file: The file to be decoded
    :param out_file: The resulting decoded file
    :param encoding: The text encoding
    """
    with open(in_file, 'r', encoding=encoding) as f_in_file:
        with open(out_file, 'w', encoding=encoding) as f_out_file:
            data = base64.b64decode(f_in_file.read())
            return f_out_file.write(str(data, encoding=encoding))


def encrypt(
    in_file: str,
    out_file: str,
    pass_phrase: str,
    salt: str = DEFAULT_HS_SALT,
    digest_algo=hashes.SHA256(),
    length=32,
    iterations=100000,
    encoding: str = 'utf-8') -> None:
    """Encrypt file using Fernet cryptography
    :param in_file: The file to be encrypted
    :param out_file: The resulting encrypted file
    :param pass_phrase: The passphrase to encrypt the file
    :param salt: TODO
    :param digest_algo: The digest encrypting algorithm
    :param length: TODO
    :param iterations: TODO
    :param encoding:
    """
    kdf = PBKDF2HMAC(
        algorithm=digest_algo,
        length=length,
        salt=salt.encode(encoding),
        iterations=iterations,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(pass_phrase.encode(encoding)))
    f = Fernet(key)
    check_argument(os.path.exists(in_file), "Input file \"{}\" does not exist", in_file)
    with open(in_file, encoding=encoding) as f_in_file:
        with open(out_file, 'w', encoding=encoding) as f_out_file:
            f_out_file.write(f.encrypt(f_in_file.read().encode(encoding)).decode(encoding))
    check_state(os.path.exists(out_file), "Unable to encrypt file \"{}\"", in_file)


def decrypt(
    in_file: str,
    out_file: str,
    pass_phrase: str,
    salt: str = DEFAULT_HS_SALT,
    digest_algo=hashes.SHA256(),
    length=32,
    iterations=100000,
    encoding: str = 'utf-8') -> None:
    """Decrypt file using Fernet cryptography
    :param in_file: The file to be decrypted
    :param out_file: The resulting decrypted file
    :param pass_phrase: The passphrase to decrypt the file
    :param salt: TODO
    :param digest_algo: The digest decrypting algorithm
    :param length: TODO
    :param iterations: TODO
    :param encoding:
    """
    kdf = PBKDF2HMAC(
        algorithm=digest_algo,
        length=length,
        salt=salt.encode(encoding),
        iterations=iterations,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(pass_phrase.encode(encoding)))
    f = Fernet(key)
    check_argument(os.path.exists(in_file), "Input file \"{}\" does not exist", in_file)
    with open(in_file, encoding=encoding) as f_in_file:
        with open(out_file, 'w', encoding=encoding) as f_out_file:
            f_out_file.write(f.decrypt(f_in_file.read().encode(encoding)).decode(encoding))
    check_state(os.path.exists(out_file), "Unable to decrypt file \"{}\"", in_file)
