#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Firebase
   @package: firebase.core
      @file: agent_config.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
import logging as log
import os
from collections import defaultdict
from os.path import basename
from typing import Any, Optional

from clitt.core.tui.minput.input_validator import InputValidator
from clitt.core.tui.minput.minput import MenuInput, minput
from datasource.firebase.firebase_configuration import FirebaseConfiguration
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.config.properties import Properties
from hspylib.core.enums.charset import Charset
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import dirname, file_is_not_empty, sysout, touch_file
from hspylib.core.tools.dict_tools import get_or_default_by_key

from firebase.core.firebase_auth import FirebaseAuth
from firebase.exception.exceptions import FirebaseAuthenticationError


class AgentConfig(metaclass=Singleton):
    """Holds the firebase agent configurations."""

    def __init__(self, filename: str) -> None:
        self.app_configs = AppConfigs(dirname(filename))
        self.firebase_configs = None
        if file_is_not_empty(self.filename):
            self._load()
            log.debug("Found and loaded a Firebase configuration: %s", self)

    def __str__(self) -> str:
        return str(self.firebase_configs)

    def __repr__(self):
        return str(self)

    def __getitem__(self, item) -> Any:
        return self.app_configs[item]

    def setup(self, load_dir: str, filename: str, config_dict: dict) -> None:
        """Setup firebase from a dict configuration
        :param load_dir: the directory where to load the configurations from.
        :param filename: the configuration file name.
        :param config_dict: firebase configuration dictionary.
        """

        user = FirebaseAuth.authenticate(config_dict["PROJECT_ID"], config_dict["UID"])
        if user:
            if user.uid != config_dict["UID"]:
                raise FirebaseAuthenticationError(
                    f"Provided UID: {config_dict['UID']} is different from retrieved UID: {user.uid}"
                )
            config_dict["UID"] = user.uid
            self.firebase_configs = FirebaseConfiguration.INSTANCE or FirebaseConfiguration.of(
                load_dir, filename, config_dict
            )
            self.firebase_configs.update(dict(config_dict))
            self._save()
        else:
            raise FirebaseAuthenticationError("Unable to authenticate to Firebase (user is None)")

    def prompt(self) -> None:
        """Create a new firebase configuration by prompting the user for information."""
        config = None
        if os.path.exists(self.filename):
            config = Properties.read_properties(self.filename)
        else:
            touch_file(self.filename)
        config = config.as_dict if config else defaultdict()
        sysout("%ORANGE%### Firebase setup")
        sysout("-=" * 15 + "%EOL%%%NC%")
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label('UID') \
                .validator(InputValidator.words()) \
                .min_max_length(30, 30) \
                .dest("uid") \
                .value(get_or_default_by_key(config, 'UID', '')) \
                .build() \
            .field() \
                .label('PROJECT_ID') \
                .validator(InputValidator.anything()) \
                .min_max_length(1, 50) \
                .dest("project_id") \
                .value(get_or_default_by_key(config, 'PROJECT_ID', '')) \
                .build() \
            .field() \
                .label('EMAIL') \
                .validator(InputValidator.anything()) \
                .min_max_length(1, 50) \
                .dest("email") \
                .value(get_or_default_by_key(config, 'EMAIL', '')) \
                .build() \
            .field() \
                .label('DATABASE') \
                .validator(InputValidator.anything()) \
                .min_max_length(1, 50) \
                .dest("database") \
                .value(get_or_default_by_key(config, 'DATABASE', '')) \
                .build() \
            .build()
        result = minput(form_fields, "Please fill in your Firebase Realtime Database configs")
        # fmt: on
        if result:
            config["UID"] = result.uid
            config["PROJECT_ID"] = result.project_id
            config["EMAIL"] = result.email
            config["DATABASE"] = result.database
            self.setup(dirname(self.filename), basename(self.filename), config)

    @property
    def filename(self) -> str:
        """Return the configuration file."""
        file = self.app_configs["hhs.firebase.config.file"]
        return file if file else f"{os.getenv('HOME', os.getcwd())}/.firebase"

    @property
    def project_id(self) -> Optional[str]:
        """Return the firebase Project ID."""
        return self.firebase_configs.project_id

    @property
    def uid(self) -> Optional[str]:
        """Return the firebase User ID."""
        return self.firebase_configs.uid

    @property
    def email(self) -> Optional[str]:
        """Return the firebase user's email."""
        return self.firebase_configs.email

    @property
    def database(self) -> Optional[str]:
        """Return the firebase project database name."""
        return self.firebase_configs.database

    def url(self, db_alias: str) -> str:
        """Return the firebase project URL."""
        final_alias = db_alias.replace(".", "/")
        return self.firebase_configs.url(final_alias)

    def _load(self) -> None:
        """Load configurations from file."""
        self.firebase_configs = FirebaseConfiguration.of_file(self.filename)

    def _save(self) -> None:
        """Save current firebase configurations to file."""
        with open(self.filename, "w+", encoding=Charset.UTF_8.val) as f_config:
            f_config.write(str(self))
            sysout(f"%BLUE%Firebase configuration saved => {self.filename} !%NC%")
