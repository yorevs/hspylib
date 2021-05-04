#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.vault.src.main.core
      @file: vault.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import base64
import getpass
import logging as log
import os
import uuid

from hspylib.core.tools.commons import sysout, safe_del_file, file_is_not_empty, touch_file, syserr
from hspylib.modules.cli.menu.menu_utils import MenuUtils
from hspylib.modules.security.security import encrypt, decrypt
from vault.src.main.core.vault_config import VaultConfig
from vault.src.main.core.vault_service import VaultService
from vault.src.main.entity.vault_entry import VaultEntry
from vault.src.main.exception.exceptions import VaultOpenError, VaultCloseError


class Vault(object):
    """Represents the vault and it's functionalities"""

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

    def open(self) -> None:
        """Open and read the Vault file"""
        self.passphrase = self._get_passphrase()
        try:
            if not self.is_open:
                self._unlock_vault()
                log.debug("Vault open and unlocked")
        except UnicodeDecodeError as err:
            log.error("Authentication failure => {}".format(str(err)))
            MenuUtils.print_error('Authentication failure')
        except Exception as err:
            raise VaultOpenError(f"Unable to open Vault file => {self.configs.vault_file()}", err)

    def close(self) -> None:
        """Close the Vault file and cleanup temporary file_paths"""
        try:
            if self.is_open:
                self._lock_vault()
                log.debug("Vault closed and locked")
        except UnicodeDecodeError as err:
            log.error("Authentication failure => {}".format(str(err)))
            MenuUtils.print_error('Authentication failure')
        except Exception as err:
            raise VaultCloseError(f"Unable to close Vault file => {self.configs.vault_file()}", err)

    def list(self, filter_expr: str = None) -> None:
        """List all vault entries filtered by filter_expr
        :param filter_expr: The filter expression
        """
        data = self.service.list(filter_expr)
        if len(data) > 0:
            sysout("%YELLOW%{} {}%NC%"
                   .format("\n=== Listing all vault entries",
                           "matching \'{}\' ===\n".format(filter_expr) if filter_expr else "===\n"))
            for entry in data:
                sysout(entry.to_string())
        else:
            if filter_expr:
                sysout("%YELLOW%\nxXx No results to display containing '{}' xXx\n%NC%".format(filter_expr))
            else:
                sysout("%YELLOW%\nxXx Vault is empty xXx\n%NC%")
        log.debug("Vault list issued. User={}".format(getpass.getuser()))

    def add(self, key: str, hint: str, password: str) -> None:
        """Add a vault entry
        :param key: The vault entry name to be added
        :param hint: The vault entry hint to be added
        :param password: The vault entry password to be added
        """
        entry = self.service.get_by_key(key)
        if not entry:
            while not password:
                password = getpass.getpass("Type the password for '{}': ".format(key)).strip()
            entry = VaultEntry(uuid.uuid4(), key, key, password, hint)
            self.service.save(entry)
            sysout("%GREEN%\n=== Entry added ===\n\n%NC%{}".format(entry.to_string()))
        else:
            log.error("Attempt to add to Vault failed for name={}".format(key))
            syserr("### Entry specified by '{}' already exists in vault".format(key))
        log.debug("Vault add issued. User={}".format(getpass.getuser()))

    def get(self, key) -> None:
        """Display the vault entry specified by name
        :param key: The vault entry name to get
        """
        entry = self.service.get_by_key(key)
        if entry:
            sysout("\n{}".format(entry.to_string(True, True)))
        else:
            log.error("Attempt to get from Vault failed for name={}".format(key))
            syserr("### No entry specified by '{}' was found in vault".format(key))
        log.debug("Vault get issued. User={}".format(getpass.getuser()))

    def update(self, key, hint, password) -> None:
        """Update a vault entry
        :param key: The vault entry name to be updated
        :param hint: The vault entry hint to be updated
        :param password: The vault entry password to be updated
        """
        entry = self.service.get_by_key(key)
        if entry:
            if not password:
                passphrase = getpass.getpass("Type a password for '{}': ".format(key)).strip()
            else:
                passphrase = password
            upd_entry = VaultEntry(entry.uuid, key, key, passphrase, hint)
            self.service.save(upd_entry)
            sysout("%GREEN%\n=== Entry updated ===\n\n%NC%{}".format(entry.to_string()))
        else:
            log.error("Attempt to update Vault failed for name={}".format(key))
            syserr("### No entry specified by '{}' was found in vault".format(key))
        log.debug("Vault update issued. User={}".format(getpass.getuser()))

    def remove(self, key: str) -> None:
        """Remove a vault entry
        :param key: The vault entry name to be removed
        """
        entry = self.service.get_by_key(key)
        if entry:
            self.service.remove(entry)
            sysout("%GREEN%\n=== Entry removed ===\n\n%NC%{}".format(entry.to_string()))
        else:
            log.error("Attempt to remove to Vault failed for name={}".format(key))
            syserr("### No entry specified by '{}' was found in vault".format(key))
        log.debug("Vault remove issued. User={}".format(getpass.getuser()))

    def _get_passphrase(self) -> str:
        """Retrieve the vault passphrase"""
        if file_is_not_empty(self.configs.vault_file()):
            confirm_flag = False
        else:
            sysout("%ORANGE%### Your Vault '{}' file is empty.".format(self.configs.vault_file()))
            sysout("%ORANGE%>>> Enter the new passphrase for this Vault")
            confirm_flag = True
            touch_file(self.configs.vault_file())
        passphrase = self.configs.passphrase()
        if passphrase:
            return "{}:{}".format(self.configs.vault_user(), base64.b64decode(passphrase).decode("utf-8"))
        else:
            while not passphrase and not confirm_flag:
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
                        log.debug("Vault passphrase created for user={}".format(self.configs.vault_user()))
                        touch_file(self.configs.vault_file())
                        self.is_open = True
            return "{}:{}".format(self.configs.vault_user(), passphrase)

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
