#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: schema_registry.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import json
import logging as log
from typing import Optional, List

from hspylib.core.enums.http_code import HttpCode
from hspylib.core.exception.exceptions import SchemaRegistryError
from hspylib.core.tools.preconditions import check_state, check_not_none
from hspylib.modules.fetch.fetch import is_reachable, delete, get
from hspylib.modules.fetch.http_response import HttpResponse
from requests import exceptions as ex

from kafman.core.schema.registry_subject import RegistrySubject


class SchemaRegistry:
    """This class is used to manage and hold information about the schema registry server"""

    def __init__(self, url: str = None):
        self._url = url or 'localhost:8081'
        self._valid = False
        self._schema_types = []
        self._subjects = []

    def is_valid(self) -> bool:
        """Whether the schema registry was validated or not"""
        return self._valid

    def url(self) -> Optional[str]:
        """Return the schema registry url"""
        return self._url

    def set_url(self, url: str, validate_url: bool = True) -> bool:
        """Set the schema registry url"""
        self._url = url
        if validate_url and is_reachable(url):
            self._valid = True
        else:
            self._valid = False
        return self._valid

    def invalidate(self) -> None:
        """Invalidate the last schema registry validation"""
        self._valid = False

    def get_schema_types(self) -> Optional[List[str]]:
        """Return the schema types supported by the server"""
        return self._schema_types

    def get_subjects(self) -> Optional[List[str]]:
        """Return the subjects currently registered at the server"""
        return self._subjects

    def deregister(self, subjects: List[RegistrySubject]) -> None:
        """Deregister the list of subjects from the registry server"""
        for subject in subjects:
            # Invoke delete subject
            _ = delete(url=f"{self._url}/subjects/{subject.subject}/versions/{subject.version}")
            self._subjects.remove(subject.subject)

    def fetch_server_info(self) -> None:
        """Fetch information about the selected schema registry server"""
        # Fetch server supported schema types
        response = self._make_request(url=f"{self._url}/schemas/types")
        self._schema_types = response.body
        # Fetch current registered subjects
        response = self._make_request(url=f"{self._url}/subjects")
        self._subjects = json.loads(response.body)

    def fetch_subjects_info(self) -> List[RegistrySubject]:
        """Fetch information about the schema registry existing subjects"""
        subjects = []
        if self._subjects:
            # Loop through recorded subjects
            for subject in self._subjects:
                # Fetch all subject versions
                response = self._make_request(url=f"{self._url}/subjects/{subject}/versions")
                all_versions = json.loads(response.body)
                check_state(isinstance(all_versions, list))
                for v in all_versions:
                    # Fetch information about the subject version
                    subject_response = self._make_request(url=f"{self._url}/subjects/{subject}/versions/{v}")
                    check_not_none(subject_response)
                    subject = json.loads(subject_response.body)
                    subjects.append(RegistrySubject(
                        subject['schemaType'] if 'schemaType' in subject else 'AVRO',
                        subject['subject'],
                        subject['id'],
                        subject['version'],
                        json.loads(subject['schema']),
                    ))

        return subjects

    def _make_request(self, url: str, expected_codes: List[HttpCode] = None) -> HttpResponse:
        """Make a request from the registry server"""
        if self._valid:
            try:
                if not expected_codes:
                    expected_codes = [HttpCode.OK]
                log.debug("Making request to: %s and expecting codes: %s", url, str(expected_codes))
                response = get(url=url)
                check_not_none(response)
                if response.status_code not in expected_codes:
                    raise SchemaRegistryError(
                        f"Request failed. Expecting {str(expected_codes)} but was received: {response.status_code}")
                return response
            except (ex.ConnectTimeout, ex.ConnectionError, ex.ReadTimeout, ex.InvalidURL) as err:
                raise SchemaRegistryError(
                    f"Unable to fetch from {self._url}\n => {str(err)}") from err

        raise SchemaRegistryError(f"Schema registry server {url} is not valid")
