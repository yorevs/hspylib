from hspylib.core.crud.crud_service import CrudService
from hspylib.core.meta.singleton import Singleton
from vault.core.vault_repository import VaultRepository


class VaultService(CrudService, metaclass=Singleton):

    def __init__(self):
        self.repository = VaultRepository()
        super().__init__(self.repository)
