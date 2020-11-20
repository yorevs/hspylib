import base64
import getpass
import os
import sys
from typing import Tuple

from hspylib.core.tools.commons import sysout, safe_del_file, file_is_not_empty, touch_file
from hspylib.modules.security.security import lock, unlock
from hspylib.ui.cli.menu_utils import MenuUtils
from vault.core.vault_config import VaultConfig
from vault.entity.vault_entry import VaultEntry
from vault.exception.vault_open_error import VaultOpenError

# Application name, read from it's own file path
APP_NAME = os.path.basename(__file__)

# Version tuple: (major,minor,build)
VERSION = (1, 2, 0)


class Vault(object):
    """Represents the vault"""

    def __init__(self):
        self.data = {}
        self.is_open = False
        self.is_modified = False
        self.is_new = False
        self.passphrase = None
        self.configs = VaultConfig()
        self.log = self.configs.logger()

    def __str__(self):
        vault_str = ""
        for entry_key in self.data:
            vault_str += str(self.data[entry_key])
        return str(vault_str)

    def exit_handler(self, signum=0, frame=None) -> None:
        """
        Handle interruptions to shutdown gracefully
        :param signum: TODO
        :param frame: TODO
        """
        if signum != 0 and frame is not None:
            self.log.warn('Signal handler hooked signum={} frame={}'.format(signum, frame))
            sysout('')
            ret_val = 1
        else:
            self.log.info('Exit handler called')
            ret_val = signum
        self.close()
        sys.exit(ret_val)

    def get_passphrase(self) -> str:
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
                        self.is_modified = True
                        self.is_new = True
            return "{}:{}".format(self.configs.vault_user(), passphrase)

    def open(self) -> None:
        """Open and read the Vault file"""
        self.passphrase = self.get_passphrase()
        try:
            if not self.is_open:
                self.unlock_vault()
                self.log.debug("Vault open modified={} open={}".format(self.is_modified, self.is_open))
            self.read()
            self.log.debug("Vault read entries={}".format(len(self.data)))
        except UnicodeDecodeError:
            MenuUtils.print_error('Invalid vault credentials')
            self.exit_handler(1)
        except Exception as err:
            raise VaultOpenError("Unable to open Vault file: {} => {}".format(self.configs.vault_file(), err))

    def close(self) -> None:
        try:
            """Close the Vault file and cleanup temporary files"""
            if self.is_modified:
                self.save()
            if self.is_open:
                self.lock_vault()
                self.log.debug("Vault closed modified={} open={}".format(self.is_modified, self.is_open))
        except UnicodeDecodeError:
            MenuUtils.print_error('Authentication failure')
            self.exit_handler(1)
        except Exception as err:
            raise VaultOpenError("Unable to close Vault file: {} => {}".format(self.configs.vault_file(), err))

    def lock_vault(self) -> None:
        """Encrypt and then, encode the vault file"""
        if file_is_not_empty(self.configs.unlocked_vault_file()):
            lock(self.configs.unlocked_vault_file(), self.configs.vault_file(), self.passphrase)
            self.log.debug("Vault file is locked !")
        else:
            os.rename(self.configs.unlocked_vault_file(), self.configs.vault_file())
        self.is_open = False
        safe_del_file(self.configs.unlocked_vault_file())

    def unlock_vault(self) -> None:
        """Decode and then, decrypt the vault file"""
        if file_is_not_empty(self.configs.vault_file()):
            unlock(self.configs.vault_file(), self.configs.unlocked_vault_file(), self.passphrase)
            self.log.debug("Vault file is unlocked !")
        else:
            os.rename(self.configs.vault_file(), self.configs.unlocked_vault_file())
        self.is_open = True
        safe_del_file(self.configs.vault_file())

    def save(self) -> None:
        """Save the vault entries"""
        with open(self.configs.unlocked_vault_file(), 'w') as f_vault:
            for entry in self.data:
                f_vault.write(str(self.data[entry]))
            self.log.debug("Vault entries saved")

    def read(self) -> None:
        """Read all existing vault payload"""
        if os.path.exists(self.configs.unlocked_vault_file()):
            try:
                with open(self.configs.unlocked_vault_file(), 'r') as f_vault:
                    for line in f_vault:
                        if not line.strip():
                            continue
                        (key, password, hint, modified) = line.strip().split('|')
                        entry = VaultEntry(key, 'TODO', password, hint, modified)
                        self.data[key] = entry
                    self.log.debug("Vault has been read. Returned payload={}".format(len(self.data)))
            except ValueError:
                self.log.error("Attempt to read from Vault failed")
                raise TypeError("### Vault file '{}' is invalid".format(self.configs.vault_file()))

    def fetch_data(self, filter_expr) -> Tuple[list, str]:
        """Filter and sort vault payload and return the proper caption for listing them
        :param filter_expr: TODO
        """
        if filter_expr:
            data = list(filter(lambda x: filter_expr in x, self.data))
            caption = "\n=== Listing vault payload containing '{}' ===\n".format(filter_expr)
        else:
            data = list(self.data)
            caption = "\n=== Listing all vault payload ===\n"
        data.sort()
        self.log.debug(
            "Vault payload fetched. Returned payload={} filtered={}".format(len(self.data), len(self.data) - len(data)))

        return data, caption

    def list(self, filter_expr=None) -> None:
        """List all vault payload
        :param filter_expr: TODO
        """
        if len(self.data) > 0:
            (data, header) = self.fetch_data(filter_expr)
            if len(data) > 0:
                sysout("%YELLOW%{}%NC%".format(header))
                for entry_key in data:
                    sysout(self.data[entry_key].to_string())
            else:
                sysout("%YELLOW%\nxXx No results to display containing '{}' xXx\n%NC%".format(filter_expr))
        else:
            sysout("%YELLOW%\nxXx Vault is empty xXx\n%NC%")
        self.log.debug("Vault list issued. User={}".format(getpass.getuser()))

    def add(self, key: str, hint: str, password: str) -> None:
        """Add a vault entry
        :param key: TODO
        :param hint: TODO
        :param password: TODO
        """
        if key not in self.data.keys():
            while not password:
                password = getpass.getpass("Type the password for '{}': ".format(key)).strip()
            entry = VaultEntry(key, 'TODO', password, hint)
            self.data[key] = entry
            self.is_modified = True
            sysout("%GREEN%\n=== Entry added ===\n\n%NC%{}".format(entry.to_string()))
        else:
            self.log.error("Attempt to add to Vault failed for key={}".format(key))
            sysout("%RED%### Entry specified by '{}' already exists in vault".format(key))
        self.log.debug("Vault add issued. User={}".format(getpass.getuser()))

    def get(self, key) -> None:
        """Display the vault entry specified by key
        :param key: TODO
        """
        if key in self.data.keys():
            entry = self.data[key]
            sysout("%GREEN%\n{}".format(entry.to_string(True)))
        else:
            self.log.error("Attempt to get from Vault failed for key={}".format(key))
            sysout("%RED%### No entry specified by '{}' was found in vault".format(key))
        self.log.debug("Vault get issued. User={}".format(getpass.getuser()))

    def update(self, key, hint, password) -> None:
        """Update a vault entry
        :param key: TODO
        :param hint: TODO
        :param password: TODO
        """
        if key in self.data.keys():
            if not password:
                passphrase = getpass.getpass("Type a password for '{}': ".format(key)).strip()
            else:
                passphrase = password
            entry = VaultEntry(key, 'TODO', passphrase, hint)
            self.data[key] = entry
            self.is_modified = True
            sysout("%GREEN%\n=== Entry updated ===\n\n%NC%{}".format(entry.to_string()))
        else:
            self.log.error("Attempt to update Vault failed for key={}".format(key))
            sysout("%RED%### No entry specified by '{}' was found in vault".format(key))
        self.log.debug("Vault update issued. User={}".format(getpass.getuser()))

    def remove(self, key: str) -> None:
        """Remove a vault entry
        :param key: TODO
        """
        if key in self.data.keys():
            entry = self.data[key]
            del self.data[key]
            self.is_modified = True
            sysout("%GREEN%\n=== Entry removed ===\n\n%NC%{}".format(entry.to_string()))
        else:
            self.log.error("Attempt to remove to Vault failed for key={}".format(key))
            sysout("%RED%### No entry specified by '{}' was found in vault".format(key))
        self.log.debug("Vault remove issued. User={}".format(getpass.getuser()))
