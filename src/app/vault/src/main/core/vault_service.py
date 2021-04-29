from typing import Optional

from hspylib.core.crud.crud_service import CrudService
from hspylib.core.meta.singleton import Singleton
from vault.src.main.core.vault_repository import VaultRepository
from vault.src.main.entity.vault_entry import VaultEntry


class VaultService(CrudService, metaclass=Singleton):

    def __init__(self):
        self.repository = VaultRepository()
        super().__init__(self.repository)

    def get_by_key(self, key: str) -> Optional[VaultEntry]:
        """TODO
        :param key: The vault key to find
        """
        return self.repository.find_by_key(key)