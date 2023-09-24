#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Vault
   @package: vault.core
      @file: vault.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from cryptography.fernet import InvalidToken
from datasource.identity import Identity
from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.commons import file_is_not_empty, safe_delete_file, syserr, sysout, touch_file
from hspylib.core.tools.text_tools import ensure_startswith, ensure_endswith
from hspylib.modules.application.application import Application
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cache.ttl_keyring_be import TTLKeyringBE
from hspylib.modules.security.security import b64_decode, decode_file, decrypt_file, encode_file, encrypt_file
from typing import List
from vault.core.vault_config import VaultConfig
from vault.core.vault_service import VaultService
from vault.domain.vault_entry import VaultEntry
from vault.exception.exceptions import VaultCloseError, VaultExecutionException, VaultSecurityException

import binascii
import contextlib
import cryptocode
import getpass
import keyring
import logging as log
import os
import shutil
import uuid


class Vault:
    """Represents the vault and it's functionalities."""

    # Vault hash code
    _VAULT_HASHCODE = os.getenv("VAULT_HASHCODE", "e4f362fd1e02df6bc9c684c9310e3550")

    # Vault keyring cache entry
    _VAULT_CACHE_NAME = "VAULT_KEY_SERVICE"

    # Maximum authentication retries
    MAX_AUTH_RETRIES = 3

    def __init__(self, resource_dir: str) -> None:
        self._is_unlocked = False
        self._passphrase = None
        self._configs = VaultConfig(resource_dir)
        self.service = VaultService(self._configs)
        keyring.set_keyring(TTLKeyringBE())

    def __str__(self):
        data = set(self.service.list())
        vault_str = ""
        for entry in data:
            vault_str += entry.key
        return vault_str

    @property
    def configs(self) -> VaultConfig:
        return self._configs

    @contextlib.contextmanager
    def open(self) -> bool:
        """Open and read the Vault file."""
        retries = 0
        self._sanity_check()
        while not self._is_unlocked and not self._passphrase and retries < self.MAX_AUTH_RETRIES:
            self._passphrase = self._read_passphrase()
            try:
                if not self._is_unlocked:
                    self._unlock_vault()
                    log.debug("Vault open and unlocked")
                yield self._is_unlocked
            except (UnicodeDecodeError, InvalidToken, binascii.Error) as err:
                log.error("Authentication failure => %s", err)
                syserr("Authentication failure!")
                keyring.delete_password(self._VAULT_CACHE_NAME, self._configs.vault_user)
                self._passphrase = None
                retries += 1
        if self._is_unlocked:
            self.close()
        else:
            Application.exit(ExitStatus.FAILED.val)

        return self._is_unlocked

    def close(self) -> bool:
        """Close the Vault file and cleanup temporary files."""
        try:
            if self._is_unlocked:
                self._lock_vault()
                log.debug("Vault closed and locked")
        except (UnicodeDecodeError, InvalidToken, binascii.Error) as err:
            log.error("Authentication failure => %s", err)
            syserr("Authentication failure")
            return False
        except Exception as err:
            raise VaultCloseError(f"Unable to close Vault file => {self._configs.vault_file}", err) from err

        return True

    def list(self, filter_expr: List[str] = None) -> None:
        """List all vault entries filtered by filter_expr
        :param filter_expr: The entry filter expression.
        """
        data = self.service.list_by_key(filter_expr)
        if len(data) > 0:
            sysout(
                "%YELLOW%{} {}%NC%".format(
                    f"\n-=- Listing all ({len(data)}) vault entries ",
                    f"matching '{filter_expr}' -=-" if filter_expr else "-=-",
                )
            )
            for entry in data:
                sysout(entry.to_string())
        else:
            if filter_expr:
                sysout(f"%YELLOW%%EOL%-=- No results to display containing '{filter_expr}' -=-%EOL%%NC%")
            else:
                sysout("%YELLOW%%EOL%-=- Vault is empty -=-%EOL%%NC%")
        log.debug("Vault list issued. User=%s", getpass.getuser())

    def add(self, key: str, hint: str | None, password: str | None) -> None:
        """Add a vault entry
        :param key: the vault entry key to be added.
        :param hint: the vault entry hint to be added.
        :param password: the vault entry password to be added.
        """
        check_not_none(key)
        if not self.service.exists(key):
            entry = VaultEntry(Identity(VaultEntry.VaultId(uuid.uuid4().hex)), key, key, password, hint)
            if not hint or not password:
                entry = VaultEntry.prompt(entry)
            if entry:
                entry.password = self._encrypt_passphrase(entry.password)
                self.service.save(entry)
                sysout(f"%GREEN%%EOL%=== Entry saved ===%EOL%%EOL%%NC%{entry.to_string()}")
        else:
            log.error("Attempt to add to Vault failed for key=%s", key)
            syserr(f"### Entry specified by '{key}' already exists in vault")
        log.debug("Vault add issued. User=%s", getpass.getuser())

    def update(self, key: str, hint: str | None, password: str | None) -> None:
        """Update a vault entry
        :param key: the vault entry key to be updated.
        :param hint: the vault entry hint to be updated.
        :param password: the vault entry password to be updated.
        """
        check_not_none(key)
        if entry := self.service.get_by_key(key):
            entry.hint = hint if hint else entry.hint
            entry.password = password if password else self._decrypt_passphrase(entry.password)
            if not hint or not password:
                entry = VaultEntry.prompt(entry)
            if entry:
                entry.password = self._encrypt_passphrase(entry.password)
                self.service.save(entry)
                sysout(f"%GREEN%%EOL%=== Entry updated ===%EOL%%EOL%%NC%{entry.to_string()}")
        else:
            log.error("Attempt to update Vault failed for key=%s", key)
            syserr(f"### No entry specified by '{key}' was found in vault")
        log.debug("Vault update issued. User=%s", getpass.getuser())

    def get(self, key) -> None:
        """Display the vault entry specified by name
        :param key: the vault entry key to get
        """
        entry = self.service.get_by_key(key)
        if entry:
            entry.password = cryptocode.decrypt(entry.password, self._VAULT_HASHCODE)
            sysout(f"\n{entry.to_string(True, True)}")
        else:
            log.error("Attempt to get from Vault failed for key=%s", key)
            syserr(f"### No entry specified by '{key}' was found in vault ###")
        log.debug("Vault get issued. User=%s", getpass.getuser())

    def remove(self, key: str) -> None:
        """Remove a vault entry
        :param key: The vault entry key to be removed
        """
        entry = self.service.get_by_key(key)
        if entry:
            self.service.remove(entry)
            sysout(f"%GREEN%%EOL%=== Entry removed ===%EOL%%EOL%%NC%{entry.to_string()}")
        else:
            log.error("Attempt to remove to Vault failed for key=%s", key)
            syserr(f"### No entry specified by '{key}' was found in vault")
        log.debug("Vault remove issued. User=%s", getpass.getuser())

    def _encrypt_passphrase(self, passphrase: str) -> str:
        """Encrypt current assigned passphrase.
        :param passphrase: the passphrase to encrypt.
        """
        return cryptocode.encrypt(passphrase, self._VAULT_HASHCODE)

    def _decrypt_passphrase(self, passphrase: str) -> str:
        """Decrypt current assigned passphrase.
        :param passphrase: the passphrase to decrypt.
        """
        return cryptocode.decrypt(passphrase, self._VAULT_HASHCODE)

    def _read_passphrase(self) -> str:
        """Read and return the vault currently assigned passphrase."""
        passphrase, confirm_passphrase = None, False
        if file_is_not_empty(self._configs.vault_file):
            if self._configs.passphrase:
                return f"{self._configs.vault_user}:{b64_decode(self._configs.passphrase)}"
        else:
            sysout(f"%ORANGE%### Your Vault '{self._configs.vault_file}' file does not exist ###")
            sysout("%ORANGE%>>> Enter the new passphrase to create a new Vault file <<<")
            if not (confirm_passphrase := self._create_new_vault()):
                raise VaultExecutionException(f"Unable to create vault file: {self._configs.vault_file}")
        while not passphrase:
            passphrase = self._getpass(confirm_passphrase)
            if passphrase and confirm_passphrase:
                passphrase_confirm = None
                while not passphrase_confirm or passphrase_confirm != passphrase:
                    passphrase_confirm = getpass.getpass("Repeat passphrase:").strip()
                    if passphrase_confirm != passphrase:
                        syserr("### Passphrase and confirmation mismatch")
                        safe_delete_file(self._configs.vault_file)
                sysout(f"%GREEN%Passphrase successfully stored at: '{self._configs.vault_file}'")
                log.debug(
                    "Vault passphrase created for user=%s and vault=%s",
                    self._configs.vault_user,
                    self._configs.vault_file,
                )
                self._is_unlocked = True

        return f"{self._configs.vault_user}:{passphrase}"

    def _lock_vault(self) -> None:
        """Lock the vault file (encode & encrypt)."""
        if file_is_not_empty(self._configs.unlocked_vault_file):
            encoded = f"{self._configs.unlocked_vault_file}-encoded"
            encode_file(self._configs.unlocked_vault_file, encoded, binary=True)
            encrypt_file(encoded, self._configs.vault_file, self._passphrase)
            safe_delete_file(encoded)
            log.debug("Vault file is encrypted")
        else:
            os.rename(self._configs.unlocked_vault_file, self._configs.vault_file)
        self._is_unlocked = False
        safe_delete_file(self._configs.unlocked_vault_file)

    def _unlock_vault(self) -> None:
        """Unlock the vault file (decode & decrypt)."""
        if file_is_not_empty(self._configs.vault_file):
            encoded = f"{self._configs.unlocked_vault_file}-encoded"
            decrypt_file(self._configs.vault_file, encoded, self._passphrase)
            decode_file(encoded, self._configs.unlocked_vault_file, binary=True)
            safe_delete_file(encoded)
            log.debug("Vault file is decrypted")
        else:
            os.rename(self._configs.vault_file, self._configs.unlocked_vault_file)
        self._is_unlocked = True
        safe_delete_file(self._configs.vault_file)

    def _sanity_check(self) -> None:
        """Check existing vault backups and apply a rollback if required."""
        vault_file = self._configs.vault_file
        unlocked_vault_file = self._configs.unlocked_vault_file
        backup_file = ensure_endswith(ensure_startswith(f"{os.path.basename(vault_file)}", '.'), '.bak')
        backup_file = f"{os.getenv('HHS_BACKUP_DIR', os.getenv('HOME', os.getenv('TEMP', '/tmp')))}/{backup_file}"
        locked_empty = not file_is_not_empty(vault_file)
        unlocked_empty = not file_is_not_empty(unlocked_vault_file)
        if not locked_empty or not unlocked_empty:
            if not locked_empty and unlocked_empty:
                log.debug("Creating a vault backup before opening it => %s", backup_file)
                shutil.copyfile(vault_file, backup_file)
            else:
                log.warning("Vault file was found open and will be removed => %s", vault_file)
                if os.path.exists(backup_file):
                    log.warning("Restoring last backup => %s", backup_file)
                    shutil.copyfile(backup_file, vault_file)
                    safe_delete_file(unlocked_vault_file)
                else:
                    log.error("No backups found !")
                    raise VaultSecurityException(
                        "Unable to either restore or re-lock the vault file. Please manually "
                        + f' backup your secrets and remove the unlocked file "{unlocked_vault_file}"'
                    )

    def _getpass(self, skip_cache: bool) -> str:
        """Prompt for the user password or retrieved the cached one if skip cache is not set.
        :param skip_cache: whether to skip the cached password value or not.
        """
        if skip_cache or (passwd := keyring.get_password(self._VAULT_CACHE_NAME, self._configs.vault_user)) is None:
            passwd = getpass.getpass("Enter passphrase:").rstrip()
            keyring.set_password(self._VAULT_CACHE_NAME, self._configs.vault_user, passwd)
        return passwd

    def _create_new_vault(self) -> bool:
        """Create the vault SQLite DB file."""
        touch_file(self._configs.vault_file)
        self.service.create_vault_db()
        return os.path.exists(self._configs.vault_file)
