from abc import ABC
from typing import List

from requests.exceptions import HTTPError

from firebase.entity.file_entry import FileEntry
from hspylib.core.enum.http_code import HttpCode
from hspylib.core.tools.commons import sysout
from hspylib.modules.fetch.fetch import put


class FileProcessor(ABC):

    @staticmethod
    def upload_files(url: str, file_paths: List[str]) -> int:
        file_data = []
        for f_path in file_paths:
            file = FileProcessor.__read_and_encode(f_path)
            file_data.append(file)
        payload = FileProcessor.__to_json(file_data)
        response = put(url, payload)
        assert response, "Response is empty"
        if response.status_code != HttpCode.OK:
            raise HTTPError(
                '{} - Unable to upload into={} with json_string={}'.format(response.status_code, url, payload))
        else:
            sysout('File(s) [{}] successfully uploaded to {}'.format(', '.join(file_paths), url))

        return len(file_data)

    @staticmethod
    def download_files(url: str) -> int:
        file_data = []

        return len(file_data)

    @staticmethod
    def __read_and_encode(file_path: str) -> FileEntry:
        return FileEntry(file_path).encode()

    @staticmethod
    def __decode_and_write(self, file_data) -> bool:
        pass

    @staticmethod
    def __to_json(file_data: List[FileEntry]) -> str:
        return '[' + ', '.join([str(entry) for entry in file_data]) + ']'

    @staticmethod
    def __from_json(db_alias: str, file_data: str) -> List[str]:
        pass
