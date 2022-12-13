#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.firebase.core
      @file: file_processor.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from abc import ABC
from firebase.entity.file_entry import FileEntry
from fnmatch import fnmatch
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.preconditions import check_argument, check_not_none
from hspylib.core.tools.commons import syserr, sysout
from hspylib.modules.fetch.fetch import get, put
from requests.exceptions import HTTPError
from typing import List, Union

import json
import logging as log
import os


class FileProcessor(ABC):
    """Utility class to upload and download B64 encoded files"""

    @staticmethod
    def upload_files(url: str, file_paths: List[str], glob_exp: str) -> int:
        """Upload files to URL"""
        data = []
        for f_path in file_paths:
            if os.path.exists(f_path):
                if os.path.isfile(f_path):
                    sysout(f'Uploading file "{f_path}" to Firebase ...')
                    f_entry = FileProcessor._read_and_encode(f_path)
                    data.append(f_entry)
                else:
                    sysout(f'Uploading files from "{f_path}" to Firebase ...')
                    all_files = next(os.walk(f_path))[2]
                    log.debug("\nGlob: %s \nFiles: %s", glob_exp, all_files)
                    for file in all_files:
                        filename = os.path.join(f_path, file)
                        if os.path.isfile(filename) and fnmatch(file, glob_exp or "*.*"):
                            f_entry = FileProcessor._read_and_encode(filename)
                            data.append(f_entry)
            else:
                syserr(f'Input file "{f_path}" does not exist')
        if data:
            payload = FileProcessor._to_json(data)
            response = put(url, payload)
            check_not_none(response)
            if response.status_code != HttpCode.OK:
                raise HTTPError(f"{response.status_code} - Unable to upload into={url} with json_string={payload}")
            paths = ", \n  |- ".join([f.path for f in data])

            sysout(f"%GREEN%File(s) [\n  |- {paths}\n] successfully uploaded to: {url}%NC%")

            return len(data)

        sysout(f"%ORANGE%No files were uploaded from {file_paths} %NC%")

        return 0

    @staticmethod
    def download_files(url: str, destination_dir: str) -> int:
        """Download files from URL"""
        check_argument(
            destination_dir and os.path.exists(destination_dir),
            "Unable find destination directory: {}",
            destination_dir,
        )
        sysout(f'Downloading files from Firebase into "{destination_dir}" ...')
        response = get(url)
        check_not_none(response)
        check_not_none(response.body)
        if response.status_code != HttpCode.OK:
            raise HTTPError(f"{response.status_code} - Unable to download from={url} with response={response}")
        file_data = FileProcessor._from_json(response.body)
        if file_data and len(file_data) > 0:
            FileProcessor._decode_and_write(destination_dir, file_data)
            return len(file_data)

        sysout(f"%ORANGE%Database alias was not found in: {url} %NC%")

        return 0

    @staticmethod
    def _read_and_encode(file_path: str) -> FileEntry:
        """Read and B64 encode a file"""
        return FileEntry(file_path).encode()

    @staticmethod
    def _decode_and_write(destination_dir: str, data: Union[dict, List[dict]]) -> None:
        """B64 decode and write entries to file"""
        if isinstance(data, list):
            for entry in data:
                FileEntry.of(
                    f"{destination_dir}/{os.path.basename(entry['path'])}", entry["data"], entry["size"]
                ).save()
            paths = ", \n  |- ".join([f["path"] for f in data])
        elif isinstance(data, dict):
            FileEntry.of(f"{destination_dir}/{os.path.basename(data['path'])}", data["data"], data["size"]).save()
            paths = data["path"]
        else:
            raise TypeError(f"Downloaded data format is not supported: {type(data)}")

        sysout(f"%GREEN%File(s) [\n  |- {paths}\n] successfully downloaded into: {destination_dir}%NC%")

    @staticmethod
    def _to_json(file_data: List[FileEntry]) -> str:
        """Convert the file data into json format"""
        return "[" + ",".join([str(entry) for entry in file_data]) + "]"

    @staticmethod
    def _from_json(file_data: str) -> List[dict]:
        """Convert json format into file data"""
        return json.loads(file_data)
