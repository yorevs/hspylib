#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.vault.core
      @file: vault.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import base64
import binascii
import getpass
import logging as log
import os
import shutil
import uuid

import cryptocode
from cryptography.fernet import InvalidToken
from hspylib.core.tools.commons import file_is_not_empty, safe_del_file, syserr, sysout, touch_file
from hspylib.modules.cli.tui.menu.menu_utils import MenuUtils
from hspylib.modules.security.security import decrypt, encrypt

from vault.core.vault_config import VaultConfig
from vault.core.vault_service import VaultService
from vault.entity.vault_entry import VaultEntry
from vault.exception.exceptions import VaultCloseError, VaultOpenError, VaultSecurityException


class Vault:
    """Represents the vault and it's functionalities"""

    # Vault hash code
    _VAULT_HASHCODE = os.getenv('VAULT_HASHCODE', 'e4f362fd1e02df6bc9c684c9310e3550')

    def __init__(self):
        self.is_open = False
        self.passphrase = None
        self.configs = VaultConfig()
        self.service = VaultService()

    def __str__(self):
        data = set(self.service.list())
        vault_str = ""
        for entry in data:
            vault_str += entry.key
        return vault_str

    def open(self) -> bool:
        """Open and read the Vault file"""
        try:
            self._check_backup()
            self.passphrase = self._read_passphrase()
            if not self.is_open:
                self._unlock_vault()
                log.debug("Vault open and unlocked")
        except (UnicodeDecodeError, InvalidToken, binascii.Error) as err:
            log.error("Authentication failure => %s", err)
            MenuUtils.print_error('Authentication failure')
            return False
        except Exception as err:
            raise VaultOpenError(f"Unable to open Vault file => {self.configs.vault_file()}", err) from err

        return True

    def close(self) -> bool:
        """Close the Vault file and cleanup temporary file_paths"""
        try:
            if self.is_open:
                self._lock_vault()
                log.debug("Vault closed and locked")
        except (UnicodeDecodeError, InvalidToken) as err:
            log.error("Authentication failure => %s", err)
            MenuUtils.print_error('Authentication failure')
            return False
        except Exception as err:
            raise VaultCloseError(f"Unable to close Vault file => {self.configs.vault_file()}", err) from err

        return True

    def list(self, filter_expr: str = None) -> None:
        """List all vault entries filtered by filter_expr
        :param filter_expr: The filter expression
        """
        data = self.service.list(filter_expr)
        if len(data) > 0:
            sysout("%YELLOW%{} {}%NC%".format(
                f"\n=== Listing all ({len(data)}) vault entries",
                f"matching \'{filter_expr}\' ===\n" if filter_expr else "===\n"))
            for entry in data:
                sysout(entry.to_string())
        else:
            if filter_expr:
                sysout(f"%YELLOW%\nxXx No results to display containing '{filter_expr}' xXx\n%NC%")
            else:
                sysout("%YELLOW%\nxXx Vault is empty xXx\n%NC%")
        log.debug("Vault list issued. User=%s", getpass.getuser())

    def add(self, key: str, hint: str, password: str) -> None:
        """Add a vault entry
        :param key: The vault entry name to be added
        :param hint: The vault entry hint to be added
        :param password: The vault entry password to be added
        """
        entry = self.service.get_by_key(key)
        if not entry:
            while not password:
                password = getpass.getpass(f"Type the password for '{key}': ").strip()
            entry = VaultEntry(uuid.uuid4(), key, key, self._get_password(password), hint)
            self.service.save(entry)
            sysout(f"%GREEN%\n=== Entry added ===\n\n%NC%{entry.to_string()}")
        else:
            log.error("Attempt to add to Vault failed for name=%s", key)
            syserr(f"### Entry specified by '{key}' already exists in vault")
        log.debug("Vault add issued. User=%s", getpass.getuser())

    def update(self, key, hint, password) -> None:
        """Update a vault entry
        :param key: The vault entry name to be updated
        :param hint: The vault entry hint to be updated
        :param password: The vault entry password to be updated
        """
        entry = self.service.get_by_key(key)
        if entry:
            while not password:
                password = getpass.getpass(f"Type a password for '{key}': ").strip()
            upd_entry = VaultEntry(entry.uuid, key, key, self._get_password(password), hint)
            self.service.save(upd_entry)
            sysout(f"%GREEN%\n=== Entry updated ===\n\n%NC%{entry.to_string()}")
        else:
            log.error("Attempt to update Vault failed for name=%s", key)
            syserr(f"### No entry specified by '{key}' was found in vault")
        log.debug("Vault update issued. User=%s", getpass.getuser())

    def get(self, key) -> None:
        """Display the vault entry specified by name
        :param key: The vault entry name to get
        """
        entry = self.service.get_by_key(key)
        if entry:
            entry.password = cryptocode.decrypt(entry.password, self._VAULT_HASHCODE)
            sysout(f"\n{entry.to_string(True, True)}")
        else:
            log.error("Attempt to get from Vault failed for name=%s", key)
            syserr(f"### No entry specified by '{key}' was found in vault")
        log.debug("Vault get issued. User=%s", getpass.getuser())

    def remove(self, key: str) -> None:
        """Remove a vault entry
        :param key: The vault entry name to be removed
        """
        entry = self.service.get_by_key(key)
        if entry:
            self.service.remove(entry)
            sysout(f"%GREEN%\n=== Entry removed ===\n\n%NC%{entry.to_string()}")
        else:
            log.error("Attempt to remove to Vault failed for name=%s", key)
            syserr(f"### No entry specified by '{key}' was found in vault")
        log.debug("Vault remove issued. User=%s", getpass.getuser())

    def _get_password(self, password: str):
        return cryptocode.encrypt(password, self._VAULT_HASHCODE)

    def _read_passphrase(self) -> str:
        """Retrieve and read the vault passphrase"""
        if os.path.exists(self.configs.vault_file()):
            confirm_flag = False
        else:
            sysout(f"%ORANGE%### Your Vault '{self.configs.vault_file()}' file is empty.")
            sysout("%ORANGE%>>> Enter the new passphrase for this Vault")
            confirm_flag = True
            touch_file(self.configs.vault_file())
        passphrase = self.configs.passphrase()
        if passphrase:
            return f"{self.configs.vault_user()}:{base64.b64decode(passphrase).decode('utf-8')}"

        while not passphrase:
            passphrase = getpass.getpass("Enter passphrase:").strip()
            confirm = None
            if passphrase and confirm_flag:
                while not confirm:
                    confirm = getpass.getpass("Repeat passphrase:").strip()
                if confirm != passphrase:
                    syserr("### Passphrase and confirmation mismatch")
                    safe_del_file(self.configs.vault_file())
                else:
                    sysout("%GREEN%Passphrase successfully stored")
                    log.debug("Vault passphrase created for user=%s", self.configs.vault_user())
                    self.is_open = True
        return f"{self.configs.vault_user()}:{passphrase}"

    def _lock_vault(self) -> None:
        """Encrypt the vault file"""
        if file_is_not_empty(self.configs.unlocked_vault_file()):
            encrypt(
                self.configs.unlocked_vault_file(),
                self.configs.vault_file(),
                self.passphrase)
            log.debug("Vault file is encrypted")
        else:
            os.rename(self.configs.unlocked_vault_file(), self.configs.vault_file())
        self.is_open = False
        safe_del_file(self.configs.unlocked_vault_file())

    def _unlock_vault(self) -> None:
        """Decrypt the vault file"""
        if file_is_not_empty(self.configs.vault_file()):
            decrypt(
                self.configs.vault_file(),
                self.configs.unlocked_vault_file(),
                self.passphrase, )
            log.debug("Vault file is decrypted")
        else:
            os.rename(self.configs.vault_file(), self.configs.unlocked_vault_file())
        self.is_open = True
        safe_del_file(self.configs.vault_file())

    def _check_backup(self) -> None:
        vault_file = self.configs.vault_file()
        unlocked_vault_file = self.configs.unlocked_vault_file()
        backup_file = f"{os.getenv('HOME', os.getenv('TEMP', '/tmp'))}/.{os.path.basename(vault_file)}.bak"
        locked_empty = not file_is_not_empty(vault_file)
        unlocked_empty = not file_is_not_empty(unlocked_vault_file)
        if locked_empty and unlocked_empty:
            return
        elif not locked_empty and unlocked_empty:
            log.debug(f'Creating a vault backup before opening it => {backup_file}')
            shutil.copyfile(vault_file, backup_file)
        elif not unlocked_empty:
            log.warning(f'Vault file was found open and will be removed => {vault_file}')
            if os.path.exists(backup_file):
                log.warning(f'Restoring last backup => {backup_file}')
                shutil.copyfile(backup_file, vault_file)
                safe_del_file(unlocked_vault_file)
            else:
                log.warning(f'No backups found !')
                raise VaultSecurityException(
                    f'Unable to either restore or re-lock the vault file. Please manually backup your secrets '
                    'and remove the unlocked file "{unlocked_vault_file}"')
