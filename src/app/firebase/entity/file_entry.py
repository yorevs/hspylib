import base64
import os
from typing import Any

from hspylib.core.enum.charset import Charset


class FileEntry:
    def __init__(self, file_path: str):
        assert os.path.exists(file_path), "File path \"{}\" does not exist".format(file_path)
        self.path = file_path
        self.size = os.path.getsize(file_path)
        with open(file_path, 'r') as f_in:
            self.data = f_in.read()
            assert len(self.data) > 0, "File \"{}\" is empty".format(file_path)

    def __str__(self) -> str:
        return '{"path" : "' + self.path + '", "size" : ' + str(self.size) + ', "data" : "' + self.data + '"}'

    def encode(self) -> Any:
        self.data = base64.urlsafe_b64encode(self.data.encode(str(Charset.UTF_8))).decode(str(Charset.UTF_8))
        return self

    def decode(self) -> Any:
        self.data = str(base64.urlsafe_b64decode(self.data.encode(str(Charset.UTF_8))))
        return self
