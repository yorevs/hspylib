#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: schema_registry.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import json
from typing import Optional, List

from requests.exceptions import ConnectTimeout, ConnectionError, InvalidURL, ReadTimeout

from hspylib.core.enums.http_code import HttpCode
from hspylib.core.exception.exceptions import SchemaRegistryError
from hspylib.core.tools.preconditions import check_state
from hspylib.modules.fetch.fetch import is_reachable, get, delete
from kafman.src.main.core.schema.registry_subject import RegistrySubject


class SchemaRegistry:
    """TODO"""

    def __init__(self, url: str = None):
        self._url = url or 'localhost:8081'
        self._valid = False
        self._schema_types = []
        self._subjects = []

    def is_valid(self) -> bool:
        """TODO"""
        return self._valid

    def url(self) -> Optional[str]:
        """TODO"""
        return self._url

    def set_url(self, url: str, validate_url: bool = True) -> bool:
        """TODO"""
        self._url = url
        if validate_url and is_reachable(url):
            self._valid = True
        else:
            self._valid = False
        return self._valid

    def invalidate(self) -> None:
        """TODO"""
        self._valid = False

    def get_schema_types(self) -> Optional[List[str]]:
        """TODO"""
        return self._schema_types

    def get_subjects(self) -> Optional[List[str]]:
        """TODO"""
        return self._subjects

    def deregister(self, subjects: List[RegistrySubject]) -> None:
        """TODO"""
        try:
            for subject in subjects:
                # Invoke delete subject
                response = delete(url=f"{self._url}/subjects/{subject.subject}/versions/{subject.version}")
                if response.status_code == HttpCode.OK:
                    self._subjects.remove(subject.subject)
                else:
                    raise SchemaRegistryError(
                        f"Unable to deregister schema subject. Response was not : {response.status_code}")
        except (ConnectTimeout, ConnectionError, ReadTimeout, InvalidURL) as err:
            raise SchemaRegistryError(
                f"Unable to fetch registry server information from {self._url}\n => {str(err)}") from err

    def fetch_server_info(self) -> None:
        """Fetch information about the selected schema registry server"""
        try:
            # Fetch server supported schema types
            response = get(url=f"{self._url}/schemas/types")
            if response.status_code == HttpCode.OK:
                self._schema_types = response.body
            elif response.status_code == HttpCode.NOT_FOUND:
                raise SchemaRegistryError('AVRO is the only supported schema type in the server')
            else:
                raise SchemaRegistryError(
                    f"Unable to fetch registry schema types. Response was not : {response.status_code}")
            # Fetch current registered subjects
            response = get(url=f"{self._url}/subjects")
            if response.status_code == HttpCode.OK:
                self._subjects = json.loads(response.body)
            else:
                raise SchemaRegistryError(
                    f"Unable to fetch registry subjects. Response was not OK: {response.status_code}")
        except (ConnectTimeout, ConnectionError, ReadTimeout, InvalidURL) as err:
            raise SchemaRegistryError(
                f"Unable to fetch registry server information from {self._url}\n => {str(err)}") from err

    def fetch_subjects_info(self) -> List[RegistrySubject]:
        """Fetch information about the schema registry existing subjects"""
        subjects = []
        if self._subjects:
            try:
                # Loop through recorded subjects
                for subject in self._subjects:
                    # Fetch all subject versions
                    response = get(url=f"{self._url}/subjects/{subject}/versions")
                    if response.status_code == HttpCode.OK:
                        all_versions = json.loads(response.body)
                        check_state(isinstance(all_versions, list))
                        for v in all_versions:
                            # Fetch information about the subject version
                            subject_response = get(url=f"{self._url}/subjects/{subject}/versions/{v}")
                            if subject_response.status_code == HttpCode.OK:
                                subject = json.loads(subject_response.body)
                                subjects.append(RegistrySubject(
                                    subject['schemaType'] if hasattr(subject, 'schemaType') else 'AVRO',
                                    subject['subject'],
                                    subject['id'],
                                    subject['version'],
                                    json.loads(subject['schema']),
                                ))
                            else:
                                raise SchemaRegistryError(
                                    f"Unable to fetch subject version. Response was not OK: {response.status_code}")
                    else:
                        raise SchemaRegistryError(
                            f"Unable to fetch registry subjects. Response was not OK: {response.status_code}")

            except (ConnectTimeout, ConnectionError, ReadTimeout, InvalidURL) as err:
                raise SchemaRegistryError(
                    f"Unable to fetch registry server information from {self._url}\n => {str(err)}") from err

        return subjects
