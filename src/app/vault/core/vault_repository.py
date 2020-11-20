import re
from typing import Optional, List

from hspylib.core.crud.file.file_repository import FileRepository
from vault.core.vault_config import VaultConfig
from vault.entity.vault_entry import VaultEntry


class VaultRepository(FileRepository):

    def __init__(self):
        self.db_file = VaultConfig.INSTANCE.unlocked_vault_file()
        super().__init__(self.db_file)

    def find_all(self, filters: str = None) -> List[VaultEntry]:
        self.storage.load()
        data = self.storage.data or []
        if data and filters:
            filtered = []
            for entry in data:
                for key in entry.values():
                    if re.search(filters, key, re.IGNORECASE):
                        filtered.append(self.dict_to_entity(entry))
                        break
            return filtered
        else:
            return [self.dict_to_entity(entry) for entry in data]

    def find_by_key(self, key: str) -> Optional[VaultEntry]:
        self.storage.load()
        if key:
            result = [data for data in self.storage.data if key == data['key']]
            assert len(result) <= 1, "Multiple results found with key={}".format(key)
            return self.dict_to_entity(result[0]) if len(result) > 0 else None
        else:
            return None

    def dict_to_entity(self, row: dict) -> VaultEntry:
        return VaultEntry(
            row['uuid'],
            row['name'],
            row['name'],
            row['hint'],
            row['modified'])
