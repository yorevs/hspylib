from hspylib.core.crud.file.file_repository import FileRepository
from vault.core.vault_config import VaultConfig
from vault.entity.vault_entry import VaultEntry


class VaultRepository(FileRepository):

    def __init__(self):
        self.db_file = VaultConfig.INSTANCE.unlocked_vault_file()
        super().__init__(self.db_file)

    def dict_to_entity(self, row: dict) -> VaultEntry:
        return VaultEntry(
            row['uuid'],
            row['name'],
            row['name'],
            row['hint'],
            row['modified'])
