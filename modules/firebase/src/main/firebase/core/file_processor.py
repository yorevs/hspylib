#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Firebase
   @package: firebase.core
      @file: file_processor.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from abc import ABC
from firebase.domain.firebase_dto import FirebaseDto
from fnmatch import fnmatch
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.preconditions import check_argument, check_not_none
from hspylib.core.tools.commons import syserr, sysout
from hspylib.modules.fetch.fetch import get, put
from requests.exceptions import HTTPError
from typing import List

import json
import logging as log
import os


class FileProcessor(ABC):
    """Utility class to upload / download B64-encoded files."""

    @staticmethod
    def upload_files(url: str, file_paths: List[str], glob_exp: str) -> int:
        """Upload files to URL.
        :param url: the URL to upload the files.
        :param file_paths: the file paths to be uploaded. File paths will be filtered by glob expressions.
        :param glob_exp: the GLOB expressions to filter the input files/folders.
        """
        data = []
        for f_path in file_paths:
            if os.path.exists(f_path):
                if os.path.isfile(f_path):
                    sysout(f"%BLUE%Uploading file  {f_path:.<22} %NC%", end="")
                    dto = FileProcessor._read_and_encode(f_path)
                    data.append(dto)
                    sysout("[%GREEN%  OK  %NC%]")
                else:
                    sysout(f'%BLUE%Uploading files from directory "{f_path}" ')
                    all_files = next(os.walk(f_path))[2]
                    log.debug("\nGlob: %s \nFiles: %s", glob_exp, all_files)
                    for file in all_files:
                        filename = os.path.join(f_path, file)
                        if os.path.isfile(filename) and fnmatch(file, glob_exp or "*.*"):
                            sysout(f"%BLUE%Uploading file  {filename:.<22} %NC%", end="")
                            dto = FileProcessor._read_and_encode(filename)
                            data.append(dto)
                            sysout("[%GREEN%  OK  %NC%]")
            else:
                syserr(f'Input file "{f_path}" does not exist!')
        if data:
            payload = FileProcessor._create_request(data)
            response = put(url, payload)
            check_not_none(response)
            if response.status_code != HttpCode.OK:
                raise HTTPError(f"{response.status_code} - Unable to upload into={url} with json_string={payload}")
            paths = " \n  |- ".join([f.path for f in data])
            sysout(f"%EOL%%GREEN%File(s):%EOL%  |- {paths}%EOL%%EOL%Successfully uploaded to Firebase!%NC%")
            return len(data)

        syserr(f"No file has been uploaded from ${file_paths}!")

        return 0

    @staticmethod
    def download_files(url: str, dest_dir: str) -> int:
        """Download files from URL.
        :param url: the URL to download the files.
        :param dest_dir: the destination directory.
        """
        check_argument(dest_dir and os.path.exists(dest_dir), "Unable find destination directory: {}", dest_dir)
        sysout(f'%BLUE%Downloading files from Firebase into "{dest_dir}" ...')
        response = get(url)
        check_not_none(response)
        check_not_none(response.body)
        if response.status_code != HttpCode.OK:
            raise HTTPError(f"{response.status_code} - Unable to download from={url} with response={response}")
        dto_list = FirebaseDto.from_json(response.body)
        if dto_list and len(dto_list) > 0:
            FileProcessor._decode_and_write(dest_dir, *dto_list)
            return len(dto_list)

        syserr(f"Database alias was not found in: {url} !")

        return 0

    @staticmethod
    def _read_and_encode(file_path: str) -> FirebaseDto:
        """Read and B64-encode a text file.
        :param file_path: the path to the encoding file.
        """
        return FirebaseDto(file_path).load().encode()

    @staticmethod
    def _decode_and_write(dest_dir: str, *data: FirebaseDto) -> None:
        """B64-decode and write entries to a text file.
        :param dest_dir: the destination directory.
        :param data: the file content to be written.
        """
        for entry in data:
            FirebaseDto.from_file(f"{dest_dir}/{os.path.basename(entry.path)}", entry.data).decode().save()
        paths = " \n  |- ".join([f.path for f in data])
        sysout(f'%EOL%%GREEN%File(s):%EOL%  |- {paths}%EOL%%EOL%Successfully downloaded into: "{dest_dir}"%NC%')

    @staticmethod
    def _create_request(entries: List[FirebaseDto]) -> str:
        """Create a Firebase request by converting a list of DTOs into JSON formatted string.
        :param entries: the file entries to be converted.
        """
        return f"[{','.join([json.dumps(e.__dict__) for e in entries])}]"
