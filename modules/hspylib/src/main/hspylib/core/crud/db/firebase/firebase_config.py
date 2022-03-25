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

   Copyright 2021, HSPyLib team
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
from hspylib.core.tools.preconditions import check_argument, check_state
from hspylib.modules.fetch.fetch import get


class FirebaseConfig(metaclass=Singleton):
    """TODO"""

    _FIREBASE_HASHCODE = '065577bcd5dde0d70d24fad7dec74a8b'

    CONFIG_FORMAT = dedent("""
    # Your Firebase configuration:
    # --------------------------
    PROJECT_ID={}
    USERNAME={}
    DATABASE={}
    PASSPHRASE={}
    """)

    @staticmethod
    def of(config_dict: CaseInsensitiveDict) -> 'FirebaseConfig':
        """TODO"""
        required_settings = ['PROJECT_ID', 'DATABASE', 'USERNAME', 'PASSPHRASE']
        check_state(
            all(k in config_dict for k in required_settings),
            "Invalid configuration file.\nMust contain all settings: {}",
            f"\t{required_settings}")
        return FirebaseConfig(
            config_dict['PROJECT_ID'],
            config_dict['DATABASE'],
            config_dict['USERNAME'],
            config_dict['PASSPHRASE'],
        )

    @staticmethod
    def of_file(filename: str, encoding: str = None) -> 'FirebaseConfig':
        """TODO"""
        check_argument(os.path.exists(filename), f"Config file does not exist: {filename}")

        with open(filename, encoding=encoding or str(Charset.UTF_8)) as f_config:
            cfg = CaseInsensitiveDict()
            for line in f_config:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                cfg[key.strip()] = value.strip()

            return FirebaseConfig.of(cfg)

    def __init__(
        self,
        project_id: str = None,
        database: str = None,
        username: str = None,
        passphrase: str = None):

        self.encoding = str(Charset.UTF_8).lower()
        self.current_state = None
        self.project_id = project_id if project_id else AppConfigs.INSTANCE['firebase.project.id']
        self.database = database if database else AppConfigs.INSTANCE['firebase.database']
        self.username = username if username else AppConfigs.INSTANCE['firebase.username']
        self.passphrase = passphrase if passphrase else AppConfigs.INSTANCE['firebase.passphrase']
        check_state(self.project_id, "Project ID must be defined")
        check_state(self.database, "Database name must be defined")
        check_state(self.username, "Username must be defined")
        self.set_passphrase()

    def __str__(self):
        return self.CONFIG_FORMAT.format(
            self.project_id,
            self.username,
            self.database,
            cryptocode.encrypt(self.passphrase, self._FIREBASE_HASHCODE)
        )

    def set_passphrase(self) -> None:
        """TODO"""
        check_state(
            self.passphrase and len(self.passphrase) >= 8,
            "Passphrase must be have least 8 characters size and must be base64 encoded")
        # self.passphrase = str(base64.b64decode(self.passphrase), encoding=self.encoding)

    def validate_config(self) -> bool:
        """TODO"""
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
        """TODO"""
        return f'https://{self.project_id}.firebaseio.com/{self.database}'

    def url(self, db_alias: str) -> str:
        """TODO"""
        final_alias_url = db_alias.replace('.', '/')
        return f'{self.base_url()}/{final_alias_url}.json'
