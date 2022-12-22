#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Datasource
   @package: datasource.firebase
      @file: firebase_configuration.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import os
from os.path import basename
from textwrap import dedent
from typing import Optional

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.enums.charset import Charset
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.preconditions import check_argument, check_not_none, check_state
from hspylib.core.tools.commons import dirname
from hspylib.modules.fetch.fetch import get
from requests.structures import CaseInsensitiveDict


class FirebaseConfiguration(AppConfigs):
    """Represents a Firebase datasource configuration"""

    CONFIG_FORMAT = dedent(
        """
    # Your Firebase configuration:
    # --------------------------
    UID={uid}
    PROJECT_ID={project_id}
    EMAIL={email}
    DATABASE={database}
    BASE_URL={base_url}
    """
    )

    REQUIRED_SETTINGS = ["UID", "PROJECT_ID", "EMAIL", "DATABASE"]

    @staticmethod
    def of(resource_dir: str, filename: str, config_dict: CaseInsensitiveDict) -> "FirebaseConfiguration":
        """Create a Firebase config from a case insensitive dictionary."""

        check_state(
            all(setting in config_dict for setting in FirebaseConfiguration.REQUIRED_SETTINGS),
            f"Invalid configuration file.\nMust contain required settings: {FirebaseConfiguration.REQUIRED_SETTINGS}",
        )
        return FirebaseConfiguration(
            resource_dir,
            filename,
            config_dict["UID"],
            config_dict["PROJECT_ID"],
            config_dict["EMAIL"],
            config_dict["DATABASE"],
        )

    @staticmethod
    def of_file(filename: str, encoding: str = Charset.UTF_8.val) -> "FirebaseConfiguration":
        """Create a Firebase config from a config file."""
        check_argument(os.path.exists(filename), f"Config file does not exist: {filename}")

        with open(filename, encoding=encoding or Charset.UTF_8.val) as f_config:
            cfg = CaseInsensitiveDict()
            for line in f_config:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key in FirebaseConfiguration.REQUIRED_SETTINGS:
                    cfg[key.strip()] = value.strip()

            return FirebaseConfiguration.of(dirname(filename), basename(filename), cfg)

    def __init__(
        self,
        resource_dir: str,
        filename: str,
        uid: str,
        project_id: str,
        email: str,
        database: Optional[str] = None,
        profile: Optional[str] = None,
    ):

        super().__init__(resource_dir, filename, profile)
        self._valid = None
        self._base_url = self["datasource.base.url"]
        self._scheme = self["datasource.scheme"] or "https"
        self._hostname = self["datasource.hostname"] or "firebaseio.com"
        self._port = self["datasource.port"] or 443 if self._scheme.endswith("s") else 80
        self._uid = uid or self["firebase.user.uid"]
        self._project_id = project_id or self["firebase.project.id"]
        self._email = email or self["firebase.email"]
        self._database = database or self["firebase.database"]

    def __str__(self) -> str:
        return (
            ""
            if not hasattr(self, "_uid")
            else self.CONFIG_FORMAT.format(
                uid=self._uid or "not-set",
                project_id=self._project_id or "not-set",
                email=self._email or "not-set",
                database=self.database or "not-set",
                base_url=self.base_url or "not-set",
            )
        )

    @property
    def hostname(self) -> str:
        return f"{self.project_id}.{self._hostname}"

    @property
    def scheme(self) -> str:
        return self._scheme

    @property
    def port(self) -> int:
        return self._port

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def project_id(self) -> str:
        return self._project_id

    @property
    def email(self) -> str:
        return self._email

    @property
    def database(self) -> Optional[str]:
        return self._database

    @property
    def base_url(self) -> str:
        return self._base_url or f"{self.scheme}://{self.hostname}:{self.port}/{self.database}"

    def validate_config(self) -> bool:
        """Validate the current configuration"""
        check_not_none(self._uid, "User UID must be defined")
        check_not_none(self._project_id, "Project ID must be defined")
        check_not_none(self._email, "Email must be defined")
        response = get(f"{self.base_url}.json")
        self._valid = response is not None and response.status_code == HttpCode.OK

        return self._valid

    def url(self, db_alias: Optional[str] = "") -> str:
        """Return the url for an element at the Firebase webapp."""
        final_alias_url = db_alias.replace(" ", "%20").replace(".", "/")
        return f"{self.base_url}/{final_alias_url}"
