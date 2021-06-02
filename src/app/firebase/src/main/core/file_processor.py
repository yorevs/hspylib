#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.firebase.src.main.core
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

from requests.exceptions import HTTPError

from firebase.src.main.entity.file_entry import FileEntry
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.tools.commons import sysout
from hspylib.modules.fetch.fetch import get, put


class FileProcessor(ABC):

    @staticmethod
    def upload_files(url: str, file_paths: List[str]) -> int:
        file_data = []
        for f_path in file_paths:
            assert os.path.exists(f_path), 'Input file "{}" does not exist'.format(f_path)
            file = FileProcessor._read_and_encode(f_path)
            file_data.append(file)
        payload = FileProcessor._to_json(file_data)
        response = put(url, payload)
        assert response, "Response is empty"
        if response.status_code != HttpCode.OK:
            raise HTTPError(
                '{} - Unable to upload into={} with json_string={}'.format(response.status_code, url, payload))
        sysout('%GREEN%File(s) [\n\t{}\n] successfully uploaded to {}%NC%'
               .format(', \n\t'.join(file_paths), url))

        return len(file_data)

    @staticmethod
    def download_files(url: str, destination_dir: str) -> int:
        assert destination_dir and os.path.exists(destination_dir), "Unable find destination directory: {}" \
            .format(destination_dir)
        response = get(url)
        assert response and response.body, "Response or response body is empty"
        if response.status_code != HttpCode.OK:
            raise HTTPError(
                '{} - Unable to download from={} with response={}'.format(response.status_code, url, response))
        file_data = FileProcessor._from_json(response.body)
        FileProcessor._decode_and_write(destination_dir, file_data)

        return len(file_data)

    @staticmethod
    def _read_and_encode(file_path: str) -> FileEntry:
        return FileEntry(file_path).encode()

    @staticmethod
    def _decode_and_write(destination_dir: str, file_entries: List[dict]) -> None:
        for entry in file_entries:
            FileEntry.of('{}/{}'.format(
                destination_dir, os.path.basename(entry['path'])),
                entry['data'],
                entry['size']).save()
            sysout('%GREEN%"{}" successfully downloaded into "{}"%NC%'.format(entry['path'], destination_dir))

    @staticmethod
    def _to_json(file_data: List[FileEntry]) -> str:
        return '[' + ', '.join([str(entry) for entry in file_data]) + ']'

    @staticmethod
    def _from_json(file_data: str) -> List[dict]:
        return json.loads(file_data)
