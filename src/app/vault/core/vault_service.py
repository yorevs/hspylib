from typing import Optional

from hspylib.core.crud.crud_service import CrudService
from hspylib.core.meta.singleton import Singleton
from vault.core.vault_repository import VaultRepository
from vault.entity.vault_entry import VaultEntry


class VaultService(CrudService, metaclass=Singleton):

    def __init__(self):
        self.repository = VaultRepository()
        super().__init__(self.repository)

    def get(self, key: str) -> Optional[VaultEntry]:
        return self.repository.find_by_key(key)
