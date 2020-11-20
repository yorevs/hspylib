import base64
import os
import subprocess

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from hspylib.core.tools.commons import safe_del_file

DEFAULT_SALT = 'HsPyLib'


# @purpose: Encode file into base64
def encode(in_file, out_file) -> int:
    with open(in_file) as f_in_file:
        with open(out_file, 'w') as f_out_file:
            b64msg = f_in_file.read().encode('utf-8')
            return f_out_file.write(str(base64.b64encode(b64msg).decode('utf-8')))


# @purpose: Decode file from base64
def decode(in_file, out_file) -> int:
    with open(in_file) as f_in_file:
        with open(out_file, 'w') as f_out_file:
            b64msg = f_in_file.read().encode('utf-8')
            return f_out_file.write(str(base64.b64decode(b64msg).decode('utf-8')))


# @purpose: Encrypt file using fernet cryptography
def encrypt(
        in_file: str,
        out_file: str,
        pass_phrase: str,
        salt: str = DEFAULT_SALT,
        digest_algo=hashes.SHA256(),
        length=32,
        iterations=100000,
        encoding: str = 'utf-8') -> None:

    kdf = PBKDF2HMAC(
        algorithm=digest_algo,
        length=length,
        salt=salt.encode(encoding),
        iterations=iterations,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(pass_phrase.encode(encoding)))
    f = Fernet(key)
    assert os.path.exists(in_file)
    with open(in_file) as f_in_file:
        with open(out_file, 'w') as f_out_file:
            f_out_file.write(f.encrypt(f_in_file.read().encode(encoding)).decode(encoding))


# @purpose: Encrypt file using fernet cryptography
def decrypt(
        in_file: str,
        out_file: str,
        pass_phrase: str,
        salt: str = DEFAULT_SALT,
        digest_algo=hashes.SHA256(),
        length=32,
        iterations=100000,
        encoding: str = 'utf-8') -> None:

    kdf = PBKDF2HMAC(
        algorithm=digest_algo,
        length=length,
        salt=salt.encode(encoding),
        iterations=iterations,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(pass_phrase.encode(encoding)))
    f = Fernet(key)
    assert os.path.exists(in_file)
    with open(in_file) as f_in_file:
        with open(out_file, 'w') as f_out_file:
            f_out_file.write(f.decrypt(f_in_file.read().encode(encoding)).decode(encoding))


# @purpose: Encrypt file using gpg
def gpg_encrypt(in_file, out_file, pass_phrase, cipher_algo='AES256', digest_algo='SHA512'):
    cmd_args = [
        'gpg', '--quiet', '--yes', '--batch'
        , '--cipher-algo={}'.format(cipher_algo)
        , '--digest-algo={}'.format(digest_algo)
        , '--passphrase={}'.format(pass_phrase)
        , '--output={}'.format(out_file), '-c', in_file
    ]
    subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)
    return '=> ' + ' '.join(cmd_args)


# @purpose: Decrypt file using gpg
def gpg_decrypt(in_file, out_file, pass_phrase, cipher_algo='AES256', digest_algo='SHA512'):
    cmd_args = [
        'gpg', '--quiet', '--yes', '--batch'
        , '--cipher-algo={}'.format(cipher_algo)
        , '--digest-algo={}'.format(digest_algo)
        , '--passphrase={}'.format(pass_phrase)
        , '--output={}'.format(out_file), in_file
    ]
    subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)
    return '=> ' + ' '.join(cmd_args)


def lock(in_file: str, out_file: str, passphrase: str, salt: str = DEFAULT_SALT, is_gpg: bool = False) -> None:
    assert os.path.exists(in_file), "Input file \"{}\" does not exist".format(in_file)
    enc_file = '{}.{}'.format(out_file, 'gpg' if is_gpg else 'fernet')
    if is_gpg:
        gpg_encrypt(in_file, enc_file, passphrase)
    else:
        encrypt(in_file, enc_file, passphrase, salt)
    assert os.path.exists(enc_file), "Unable to encrypt file {}".format(in_file)
    encode(enc_file, out_file)
    assert os.path.exists(out_file), "Unable to encode file {}".format(in_file)
    safe_del_file(enc_file)


def unlock(in_file: str, out_file: str, passphrase: str, salt: str = DEFAULT_SALT, is_gpg: bool = False) -> None:
    assert os.path.exists(in_file), "Input file \"{}\" does not exist".format(in_file)
    dec_file = '{}.{}'.format(out_file, 'gpg' if is_gpg else 'fernet')
    decode(in_file, dec_file)
    assert os.path.exists(dec_file), "Unable to decode file \"{}\"".format(in_file)
    if is_gpg:
        gpg_decrypt(dec_file, out_file, passphrase)
    else:
        decrypt(dec_file, out_file, passphrase, salt)
    assert os.path.exists(out_file), "Unable to decrypt file {}".format(in_file)
    safe_del_file(dec_file)

