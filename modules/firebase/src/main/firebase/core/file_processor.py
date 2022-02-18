#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.firebase.core
      @file: file_processor.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import json
import os
from abc import ABC
from typing import List

from firebase.entity.file_entry import FileEntry
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.preconditions import check_argument, check_not_none, check_state
from hspylib.modules.fetch.fetch import get, put
from requests.exceptions import HTTPError


class FileProcessor(ABC):
    """Utility class to upload and download B64 encoded files"""

    @staticmethod
    def upload_files(url: str, file_paths: List[str]) -> int:
        """Upload files to URL"""
        file_data = []
        for f_path in file_paths:
            check_state(os.path.exists(f_path), f'Input file "{f_path}" does not exist')
            file = FileProcessor._read_and_encode(f_path)
            file_data.append(file)
        payload = FileProcessor._to_json(file_data)
        response = put(url, payload)
        check_not_none(response)
        if response.status_code != HttpCode.OK:
            raise HTTPError(
                '{response.status_code} - Unable to upload into={url} with json_string={payload}')
        paths = ', \n\t'.join(file_paths)
        sysout(f"%GREEN%File(s) [\n\t{paths}\n] successfully uploaded to {url}%NC%")

        return len(file_data)

    @staticmethod
    def download_files(url: str, destination_dir: str) -> int:
        """Download files from URL"""
        check_argument(
            destination_dir and os.path.exists(destination_dir),
            "Unable find destination directory: {}", destination_dir)
        response = get(url)
        check_not_none(response)
        check_not_none(response.body)
        if response.status_code != HttpCode.OK:
            raise HTTPError(
                f'{response.status_code} - Unable to download from={url} with response={response}')
        file_data = FileProcessor._from_json(response.body)
        FileProcessor._decode_and_write(destination_dir, file_data)

        return len(file_data)

    @staticmethod
    def _read_and_encode(file_path: str) -> FileEntry:
        """Read and B64 encode a file"""
        return FileEntry(file_path).encode()

    @staticmethod
    def _decode_and_write(destination_dir: str, file_entries: List[dict]) -> None:
        """B64 decode and write entries to file"""
        for entry in file_entries:
            FileEntry.of(
                f"{destination_dir}/{os.path.basename(entry['path'])}",
                entry['data'],
                entry['size']).save()
        files = ', \n\t'.join(list(map(lambda e: e['path'], file_entries)))
        sysout(f'%GREEN%File(s) [\n\t{files}\n] successfully downloaded into {destination_dir}%NC%')

    @staticmethod
    def _to_json(file_data: List[FileEntry]) -> str:
        """Convert the file data into json format"""
        return '[' + ', '.join([str(entry) for entry in file_data]) + ']'

    @staticmethod
    def _from_json(file_data: str) -> List[dict]:
        """Convert json format into file data"""
        return json.loads(file_data)
