import getpass

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton


class VaultConfig(metaclass=Singleton):
    """Holds the vault configurations"""

    def __init__(self):
        self.configs = AppConfigs.INSTANCE

    def vault_user(self) -> str:
        user = self.configs['hhs.vault.user']
        return user if user else getpass.getuser()

    def passphrase(self) -> str:
        return self.configs['hhs.vault.passphrase']

    def vault_file(self) -> str:
        file = self.configs['hhs.vault.file']
        return file if file else f"{self.configs.resource_dir()}/.vault"

    def unlocked_vault_file(self) -> str:
        return f"{self.vault_file()}.unlocked"
