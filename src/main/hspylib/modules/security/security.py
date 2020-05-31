import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# @purpose: Encode file into base64
def encode(in_file, out_file):
    with open(in_file) as f_in_file:
        with open(out_file, 'w') as f_out_file:
            b64msg = f_in_file.read().encode('utf-8')
            return f_out_file.write(str(base64.b64encode(b64msg).decode('utf-8')))


# @purpose: Decode file from base64
def decode(in_file, out_file):
    with open(in_file) as f_in_file:
        with open(out_file, 'w') as f_out_file:
            b64msg = f_in_file.read().encode('utf-8')
            return f_out_file.write(str(base64.b64decode(b64msg).decode('utf-8')))


# @purpose: Encrypt file using gpg
def encrypt(
        in_file: str,
        out_file: str,
        pass_phrase: str,
        salt: str,
        digest_algo=hashes.SHA256(),
        length=32,
        iterations=100000,
        encoding: str = 'utf-8'):

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


# @purpose: Decrypt file using gpg
def decrypt(
        in_file: str,
        out_file: str,
        pass_phrase: str,
        salt: str,
        digest_algo=hashes.SHA256(),
        length=32,
        iterations=100000,
        encoding: str = 'utf-8'):

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
