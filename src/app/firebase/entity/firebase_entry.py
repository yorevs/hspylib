import json
from datetime import datetime
from typing import Any, List

from firebase.entity.file_entry import FileEntry
from hspylib.core.enum.charset import Charset


class FirebaseEntry:

    @staticmethod
    def of(json_string: str) -> Any:
        entry = FirebaseEntry()
        return entry

    def __init__(self,
                 name: str = None,
                 last_update_user: str = None,
                 files: List[FileEntry] = None,
                 encoding: Charset = Charset.UTF_8):
        self.name = name
        self.last_update_user = last_update_user
        self.files = files if files else []
        self.str_encoding = str(encoding).lower()
        self.last_modified = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def __str__(self):
        return json.dumps(self.__dict__)

    def payload(self) -> str:
        return str({
            'encoding': self.str_encoding,
            'file_paths': str(self.files),
            'last_modified': self.last_modified,
            'last_update_user': self.last_update_user
        })
