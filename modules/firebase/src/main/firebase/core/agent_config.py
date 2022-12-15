#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.firebase.core
      @file: agent_config.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from datasource.firebase.firebase_configuration import FirebaseConfiguration
from firebase.core.firebase_auth import FirebaseAuth
from firebase.exception.exceptions import FirebaseAuthenticationError
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import dirname, file_is_not_empty, sysout
from requests.structures import CaseInsensitiveDict
from typing import Any, Optional

import logging as log
import os


class AgentConfig(metaclass=Singleton):
    """Holds the firebase agent configurations"""

    def __init__(self) -> None:
        self.app_configs = AppConfigs()
        self.firebase_configs = None
        if file_is_not_empty(self.filename):
            self._load()
            log.debug("Found and loaded a Firebase configuration: %s", self)

    def __str__(self) -> str:
        return str(self.firebase_configs or "")

    def __repr__(self):
        return str(self)

    def __getitem__(self, item) -> Any:
        return self.app_configs[item]

    @property
    def hash_str(self) -> str:
        return "f6680e84-12c0-459c-8cf9-bd469def750d"

    def setup(self, resource_dir: str, filename: str, config_dict: CaseInsensitiveDict) -> None:
        """Setup firebase from a dict configuration
        :param filename:
        :param resource_dir:
        :param config_dict: Firebase configuration dictionary
        """

        user = FirebaseAuth.authenticate(config_dict["PROJECT_ID"], config_dict["UUID"])
        if user:
            if user.uid != config_dict["UUID"]:
                raise FirebaseAuthenticationError(
                    f"Provided UID: {config_dict['UUID']} is different from retrieved UID: {user.uid}"
                )
            config_dict["UUID"] = user.uid
            self.firebase_configs = FirebaseConfiguration.of(resource_dir, filename, config_dict)
            self._save()
        else:
            raise FirebaseAuthenticationError("Unable to authenticate to Firebase (user is None)")

    def prompt(self) -> None:
        """Create a new firebase configuration by prompting the user for information."""
        config = CaseInsensitiveDict()
        sysout("### Firebase setup")
        sysout("-=" * 15)
        config["UUID"] = self.uuid
        config["PROJECT_ID"] = self.project_id
        config["DATABASE"] = self.database
        config["EMAIL"] = self.email
        self.setup(dirname(self.filename), self.filename, config)

    @property
    def filename(self) -> str:
        """Return the configuration file."""
        file = self.app_configs["hhs.firebase.config.file"]
        return file if file else f"{os.getenv('HOME', os.getcwd())}/.firebase"

    @property
    def project_id(self) -> Optional[str]:
        """Return the firebase project ID."""
        pid = self.app_configs["hhs.firebase.project.id"]
        return pid if pid else input("Please type your project ID: ")

    @property
    def uuid(self) -> Optional[str]:
        """Return the firebase user ID."""
        uid = self.app_configs["hhs.firebase.user.uid"]
        return uid if uid else input("Please type your user UID: ")

    @property
    def email(self) -> Optional[str]:
        """Return the firebase username."""
        em = self.app_configs["hhs.firebase.email"]
        return em if em else input("Please type your Email: ")

    @property
    def database(self) -> Optional[str]:
        """Return the firebase project database name."""
        database = self.app_configs["hhs.firebase.database"]
        return database if database else input("Please type your database Name: ")

    def url(self, db_alias: str) -> str:
        """Return the firebase project URL"""
        final_alias = db_alias.replace(".", "/")
        return self.firebase_configs.url(final_alias)

    def _load(self) -> None:
        """Load configuration from file"""
        self.firebase_configs = FirebaseConfiguration.of_file(self.filename)

    def _save(self) -> None:
        """Save current firebase configuration"""
        with open(self.filename, "w+", encoding="utf-8") as f_config:
            f_config.write(str(self))
            sysout(f"Firebase configuration saved => {self.filename} !")
