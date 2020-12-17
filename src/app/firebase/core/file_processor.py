import json
from abc import ABC
from typing import List

from requests.exceptions import HTTPError

from firebase.entity.file_entry import FileEntry
from hspylib.core.enum.http_code import HttpCode
from hspylib.core.tools.commons import sysout
from hspylib.modules.fetch.fetch import put, get


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
    def download_files(url: str, dest_dir: str) -> int:
        response = get(url)
        assert response and response.body, "Response or response body is empty"
        if response.status_code != HttpCode.OK:
            raise HTTPError(
                '{} - Unable to download from={} with response={}'.format(response.status_code, url, response))
        file_data = FileProcessor.__from_json(response.body)
        FileProcessor.__decode_and_write(file_data)

        return len(file_data)

    @staticmethod
    def __read_and_encode(file_path: str) -> FileEntry:
        return FileEntry(file_path).encode()

    @staticmethod
    def __decode_and_write(file_entries: List[dict]) -> bool:
        for entry in file_entries:
            ff = FileEntry.of(entry['path'], entry['data'], entry['size'])
            print('Data: {}, Size: {}, Path: {}'.format(entry['data'], entry['size'], entry['path']))
        return True

    @staticmethod
    def __to_json(file_data: List[FileEntry]) -> str:
        return '[' + ', '.join([str(entry) for entry in file_data]) + ']'

    @staticmethod
    def __from_json(file_data: str) -> List[dict]:
        return json.loads(file_data)
