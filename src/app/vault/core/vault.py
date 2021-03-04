import base64
import getpass
import os
import uuid

from hspylib.core.tools.commons import sysout, safe_del_file, file_is_not_empty, touch_file
from hspylib.modules.security.security import encrypt, decrypt
from hspylib.ui.cli.menu.menu_utils import MenuUtils
from vault.core.vault_config import VaultConfig
from vault.core.vault_service import VaultService
from vault.entity.vault_entry import VaultEntry
from vault.exception.vault_close_error import VaultCloseError
from vault.exception.vault_open_error import VaultOpenError

# Application name, read from it's own file path
APP_NAME = os.path.basename(__file__)

# Version tuple: (major,minor,build)
VERSION = (1, 2, 0)


class Vault(object):
    """Represents the vault and it's functionalities"""

    def __init__(self):
        self.is_open = False
        self.passphrase = None
        self.configs = VaultConfig()
        self.service = VaultService()
        self.log = self.configs.logger()

    def __str__(self):
        data = self.service.list()
        vault_str = ""
        for entry in data:
            vault_str += entry.key
        return vault_str

    def exit_handler(self, signum=0, frame=None) -> None:
        """
        Handle interruptions to shutdown gracefully
        :param signum: The signal number or the exit code
        :param frame: The frame raised by the signal
        """
        if frame is not None:
            self.log.warn('Signal handler hooked signum={} frame={}'.format(signum, frame))
            exit_code = 3
        else:
            self.log.info('Exit handler called')
            exit_code = signum
        self.close()
        sysout('')
        exit(exit_code)

    def open(self) -> None:
        """Open and read the Vault file"""
        self.passphrase = self.__get_passphrase()
        try:
            if not self.is_open:
                self.__unlock_vault()
                self.log.debug("Vault open and unlocked")
        except UnicodeDecodeError as err:
            self.log.error("Authentication failure => {}".format(str(err)))
            MenuUtils.print_error('Authentication failure')
        except Exception as err:
            raise VaultOpenError("Unable to open Vault file => {}".format(str(err)))

    def close(self) -> None:
        """Close the Vault file and cleanup temporary file_paths"""
        try:
            if self.is_open:
                self.__lock_vault()
                self.log.debug("Vault closed and locked")
        except UnicodeDecodeError as err:
            self.log.error("Authentication failure => {}".format(str(err)))
            MenuUtils.print_error('Authentication failure')
        except Exception as err:
            raise VaultCloseError("Unable to close Vault file => {}".format(str(err)))

    def list(self, filter_expr: str = None) -> None:
        """List all vault entries filtered by filter_expr
        :param filter_expr: The filter expression
        """
        try:
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
            self.log.debug("Vault list issued. User={}".format(getpass.getuser()))
        except Exception as err:
            self.close()
            raise VaultOpenError("Unable to list Vault entries => {}".format(str(err)))

    def add(self, key: str, hint: str, password: str) -> None:
        """Add a vault entry
        :param key: The vault entry name to be added
        :param hint: The vault entry hint to be added
        :param password: The vault entry password to be added
        """
        entry = self.service.get(key)
        if not entry:
            while not password:
                password = getpass.getpass("Type the password for '{}': ".format(key)).strip()
            entry = VaultEntry(uuid.uuid4(), key, key, password, hint)
            self.service.save(entry)
            sysout("%GREEN%\n=== Entry added ===\n\n%NC%{}".format(entry.to_string()))
        else:
            self.log.error("Attempt to add to Vault failed for name={}".format(key))
            sysout("%RED%### Entry specified by '{}' already exists in vault".format(key))
        self.log.debug("Vault add issued. User={}".format(getpass.getuser()))

    def get(self, key) -> None:
        """Display the vault entry specified by name
        :param key: The vault entry name to get
        """
        entry = self.service.get(key)
        if entry:
            sysout("%GREEN%\n{}".format(entry.to_string(True, True)))
        else:
            self.log.error("Attempt to get from Vault failed for name={}".format(key))
            sysout("%RED%### No entry specified by '{}' was found in vault".format(key))
        self.log.debug("Vault get issued. User={}".format(getpass.getuser()))

    def update(self, key, hint, password) -> None:
        """Update a vault entry
        :param key: The vault entry name to be updated
        :param hint: The vault entry hint to be updated
        :param password: The vault entry password to be updated
        """
        entry = self.service.get(key)
        if entry:
            if not password:
                passphrase = getpass.getpass("Type a password for '{}': ".format(key)).strip()
            else:
                passphrase = password
            upd_entry = VaultEntry(entry.uuid, key, key, passphrase, hint)
            self.service.save(upd_entry)
            sysout("%GREEN%\n=== Entry updated ===\n\n%NC%{}".format(entry.to_string()))
        else:
            self.log.error("Attempt to update Vault failed for name={}".format(key))
            sysout("%RED%### No entry specified by '{}' was found in vault".format(key))
        self.log.debug("Vault update issued. User={}".format(getpass.getuser()))

    def remove(self, key: str) -> None:
        """Remove a vault entry
        :param key: The vault entry name to be removed
        """
        entry = self.service.get(key)
        if entry:
            self.service.remove(entry)
            sysout("%GREEN%\n=== Entry removed ===\n\n%NC%{}".format(entry.to_string()))
        else:
            self.log.error("Attempt to remove to Vault failed for name={}".format(key))
            sysout("%RED%### No entry specified by '{}' was found in vault".format(key))
        self.log.debug("Vault remove issued. User={}".format(getpass.getuser()))

    def __get_passphrase(self) -> str:
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
                        sysout("%RED%### Passphrase and confirmation mismatch")
                        safe_del_file(self.configs.vault_file())
                    else:
                        sysout("%GREEN%Passphrase successfully stored")
                        self.log.debug("Vault passphrase created for user={}".format(self.configs.vault_user()))
                        touch_file(self.configs.vault_file())
                        self.is_open = True
            return "{}:{}".format(self.configs.vault_user(), passphrase)

    def __lock_vault(self) -> None:
        """Encrypt the vault file"""
        if file_is_not_empty(self.configs.unlocked_vault_file()):
            encrypt(
                self.configs.unlocked_vault_file(),
                self.configs.vault_file(),
                self.passphrase)
            self.log.debug("Vault file is encrypted")
        else:
            os.rename(self.configs.unlocked_vault_file(), self.configs.vault_file())
        self.is_open = False
        safe_del_file(self.configs.unlocked_vault_file())

    def __unlock_vault(self) -> None:
        """Decrypt the vault file"""
        if file_is_not_empty(self.configs.vault_file()):
            decrypt(
                self.configs.vault_file(),
                self.configs.unlocked_vault_file(),
                self.passphrase,)
            self.log.debug("Vault file is decrypted")
        else:
            os.rename(self.configs.vault_file(), self.configs.unlocked_vault_file())
        self.is_open = True
        safe_del_file(self.configs.vault_file())
