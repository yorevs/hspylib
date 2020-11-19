import getpass
from logging import log

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton


class VaultConfig(metaclass=Singleton):
    """Holds the vault configurations"""

    def __init__(self):
        self.configs = AppConfigs.INSTANCE

    def logger(self) -> log:
        return self.configs.logger()

    def vault_user(self):
        user = self.configs.get('hhs.vault.user')
        return user if user else getpass.getuser()

    def vault_file(self):
        file = self.configs.get('hhs.vault.file')
        return file if file else '{}/.vault'.format(self.configs.resource_dir())

    def unlocked_vault_file(self):
        return "{}.unlocked".format(self.vault_file())

    def passphrase(self):
        return self.configs.get('hhs.vault.passphrase')
