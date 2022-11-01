#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.crud.db.firebase
      @file: firebase_config.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import logging as log
import os
from textwrap import dedent

import cryptocode
from requests.structures import CaseInsensitiveDict

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.enums.charset import Charset
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_argument, check_state
from hspylib.modules.fetch.fetch import get


class FirebaseConfig(metaclass=Singleton):
    """Represents a Firebase project configuration"""

    _FIREBASE_HASHCODE = '065577bcd5dde0d70d24fad7dec74a8b'

    CONFIG_FORMAT = dedent("""
    # Your Firebase configuration:
    # --------------------------
    UUID={}
    PROJECT_ID={}
    EMAIL={}
    DATABASE={}
    PASSPHRASE={}
    """)

    REQUIRED_SETTINGS = ['UUID', 'PROJECT_ID', 'EMAIL', 'DATABASE', 'PASSPHRASE']

    @staticmethod
    def of(config_dict: CaseInsensitiveDict) -> 'FirebaseConfig':
        """Create a Firebase config from a case insensitive dictionary."""
        check_state(
            all(k in config_dict for k in FirebaseConfig.REQUIRED_SETTINGS),
            "Invalid configuration file.\nMust contain all settings: {}",
            f"\t{FirebaseConfig.REQUIRED_SETTINGS}")
        return FirebaseConfig(
            config_dict['UUID'],
            config_dict['PROJECT_ID'],
            config_dict['EMAIL'],
            config_dict['DATABASE'],
            config_dict['PASSPHRASE'],
        )

    @staticmethod
    def of_file(filename: str, encoding: str = str(Charset.UTF_8)) -> 'FirebaseConfig':
        """Create a Firebase config from a config file."""
        check_argument(os.path.exists(filename), f"Config file does not exist: {filename}")

        with open(filename, encoding=encoding or str(Charset.UTF_8)) as f_config:
            cfg = CaseInsensitiveDict()
            for line in f_config:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key in FirebaseConfig.REQUIRED_SETTINGS:
                    cfg[key.strip()] = value.strip()

            return FirebaseConfig.of(cfg)

    def __init__(
        self,
        uuid: str,
        project_id: str,
        database: str,
        username: str,
        passphrase: str):

        self.current_state = None
        self.uuid = uuid if uuid else AppConfigs.INSTANCE['firebase.user.uid']
        self.project_id = project_id if project_id else AppConfigs.INSTANCE['firebase.project.id']
        self.email = username if username else AppConfigs.INSTANCE['firebase.email']
        self.database = database if database else AppConfigs.INSTANCE['firebase.database']
        self.passphrase = passphrase if passphrase else AppConfigs.INSTANCE['firebase.passphrase']
        check_state(self.uuid, "User UID must be defined")
        check_state(self.project_id, "Project ID must be defined")
        check_state(self.email, "Email must be defined")
        check_state(self.database, "Database name must be defined")
        check_state(self.passphrase, "Passphrase must be defined")
        self.decode_passphrase()

    def __str__(self) -> str:
        return self.CONFIG_FORMAT.format(
            self.uuid,
            self.project_id,
            self.email,
            self.database,
            cryptocode.encrypt(self.passphrase, self._FIREBASE_HASHCODE)
        )

    def decode_passphrase(self) -> None:
        """Set a passphrase for the Firebase connection."""
        check_state(
            self.passphrase and len(self.passphrase) >= 8,
            "Passphrase must be have least 8 characters size")
        self.passphrase = cryptocode.decrypt(self.passphrase, self._FIREBASE_HASHCODE)

    def validate_config(self) -> bool:
        """Validate the current configuration"""
        response = get(f'{self.base_url()}.json')
        is_valid = response is not None and response.status_code == HttpCode.OK
        if is_valid:
            self.current_state = response.body if response.body and response.body != 'null' else None
            log.debug("Successfully connected to Firebase: %s", self.base_url())
        else:
            self.current_state = None
            log.error("Your Firebase configuration is not valid")

        return is_valid

    def base_url(self) -> str:
        """Return the url for the project at the Firebase webapp."""
        return f'https://{self.project_id}.firebaseio.com/{self.database}'

    def url(self, db_alias: str) -> str:
        """Return the url for an element at the Firebase webapp."""
        final_alias_url = db_alias.replace('.', '/')
        return f'{self.base_url()}/{final_alias_url}.json'

    def as_dict(self) -> CaseInsensitiveDict:
        """TODO"""
        return CaseInsensitiveDict(self.__dict__)
