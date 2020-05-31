import base64
import subprocess


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
def encrypt(in_file, out_file, pass_phrase, cipher_algo='AES256', digest_algo='SHA512'):
    cmd_args = [
        'gpg', '--quiet', '--yes', '--batch',
        '--cipher-algo={}'.format(cipher_algo),
        '--digest-algo={}'.format(digest_algo),
        '--passphrase={}'.format(pass_phrase),
        '--output={}'.format(out_file), '-c', in_file
    ]
    subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)
    return '=> ' + ' '.join(cmd_args)


# @purpose: Decrypt file using gpg
def decrypt(in_file, out_file, pass_phrase, cipher_algo='AES256', digest_algo='SHA512'):
    cmd_args = [
        'gpg', '--quiet', '--yes', '--batch',
        '--cipher-algo={}'.format(cipher_algo),
        '--digest-algo={}'.format(digest_algo),
        '--passphrase={}'.format(pass_phrase),
        '--output={}'.format(out_file), in_file
    ]
    subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)
    return '=> ' + ' '.join(cmd_args)
