import base64
import os
import subprocess

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from hspylib.core.tools.commons import safe_del_file

DEFAULT_SALT = 'HsPyLib'


def encode(in_file, out_file) -> int:
    """Encode file into base64
    :param in_file: The file to be encoded
    :param out_file: The resulting encoded file
    """
    with open(in_file) as f_in_file:
        with open(out_file, 'w') as f_out_file:
            b64msg = f_in_file.read().encode('utf-8')
            return f_out_file.write(str(base64.b64encode(b64msg).decode('utf-8')))


def decode(in_file, out_file) -> int:
    """Decode file from base64
    :param in_file: The file to be decoded
    :param out_file: The resulting decoded file
    """
    with open(in_file) as f_in_file:
        with open(out_file, 'w') as f_out_file:
            b64msg = f_in_file.read().encode('utf-8')
            return f_out_file.write(str(base64.b64decode(b64msg).decode('utf-8')))


def encrypt(
        in_file: str,
        out_file: str,
        pass_phrase: str,
        salt: str = DEFAULT_SALT,
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
    assert os.path.exists(in_file)
    with open(in_file) as f_in_file:
        with open(out_file, 'w') as f_out_file:
            f_out_file.write(f.encrypt(f_in_file.read().encode(encoding)).decode(encoding))


def decrypt(
        in_file: str,
        out_file: str,
        pass_phrase: str,
        salt: str = DEFAULT_SALT,
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
    assert os.path.exists(in_file)
    with open(in_file) as f_in_file:
        with open(out_file, 'w') as f_out_file:
            f_out_file.write(f.decrypt(f_in_file.read().encode(encoding)).decode(encoding))


def gpg_encrypt(
        in_file: str,
        out_file: str,
        pass_phrase: str,
        cipher_algo='AES256',
        digest_algo='SHA512') -> str:
    """Encrypt file using gpg
    :param in_file: The file to be encrypted
    :param out_file: The resulting encrypted file
    :param pass_phrase: The passphrase to encrypt the file
    :param cipher_algo: The cipher algorithm
    :param digest_algo: The digest encrypting algorithm
    """
    cmd_args = [
        'gpg', '--quiet', '--yes', '--batch'
        , '--cipher-algo={}'.format(cipher_algo)
        , '--digest-algo={}'.format(digest_algo)
        , '--passphrase={}'.format(pass_phrase)
        , '--output={}'.format(out_file), '-c', in_file
    ]
    subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)
    return '=> ' + ' '.join(cmd_args)


def gpg_decrypt(
        in_file: str,
        out_file: str,
        pass_phrase: str,
        cipher_algo='AES256',
        digest_algo='SHA512'):
    """Decrypt file using gpg
    :param in_file: The file to be decrypted
    :param out_file: The resulting decrypted file
    :param pass_phrase: The passphrase to decrypt the file
    :param cipher_algo: The cipher algorithm
    :param digest_algo: The digest decrypting algorithm
    """
    cmd_args = [
        'gpg', '--quiet', '--yes', '--batch'
        , '--cipher-algo={}'.format(cipher_algo)
        , '--digest-algo={}'.format(digest_algo)
        , '--passphrase={}'.format(pass_phrase)
        , '--output={}'.format(out_file), in_file
    ]
    subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)
    return '=> ' + ' '.join(cmd_args)


def lock(
        in_file: str,
        out_file: str,
        passphrase: str,
        salt: str = DEFAULT_SALT,
        is_gpg: bool = False) -> None:
    """ TODO
    :param in_file:
    :param out_file:
    :param passphrase:
    :param salt:
    :param is_gpg:
    """
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


def unlock(
        in_file: str,
        out_file: str,
        passphrase: str,
        salt: str = DEFAULT_SALT,
        is_gpg: bool = False) -> None:
    """ TODO
    :param in_file:
    :param out_file:
    :param passphrase:
    :param salt:
    :param is_gpg:
    """
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
