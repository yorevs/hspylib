#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: hspylib.main.hspylib.core.crud.db.firebase
      @file: firebase_config.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import base64
import logging as log
import os
import uuid

from requests.structures import CaseInsensitiveDict

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.enums.charset import Charset
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.preconditions import check_argument, check_state
from hspylib.modules.fetch.fetch import get


class FirebaseConfig(metaclass=Singleton):
    """TODO"""

    CONFIG_FORMAT = """
# Your Firebase configuration:
# --------------------------
PROJECT_ID={}
USERNAME={}
DATABASE={}
PASSPHRASE={}
UUID={}
"""

    @staticmethod
    def of(config_dict: CaseInsensitiveDict) -> 'FirebaseConfig':
        """TODO"""
        return FirebaseConfig(
            config_dict['PROJECT_ID'],
            config_dict['DATABASE'],
            config_dict['UUID'] if 'UUID' in config_dict else None,
            config_dict['USERNAME'],
            config_dict['PASSPHRASE'],
        )

    @staticmethod
    def of_file(filename: str) -> 'FirebaseConfig':
        """TODO"""
        check_argument(os.path.exists(filename), "Config file does not exist")

        with open(filename) as f_config:
            cfg = CaseInsensitiveDict()
            for line in f_config:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                cfg[key.strip()] = value.strip()
            check_state(
                len(cfg) > 4,
                "Invalid configuration file. Must include at least: [PROJECT_ID, FIREBASE_URL, USERNAME, PASSPHRASE]")

            return FirebaseConfig.of(cfg) if len(cfg) == 5 else None

    def __init__(
        self,
        project_id: str = None,
        database: str = None,
        project_uuid: str = None,
        username: str = None,
        passphrase: str = None):

        self.encoding = str(Charset.UTF_8).lower()
        self.current_state = None
        self.project_id = project_id if project_id else AppConfigs.INSTANCE['firebase.project.id']
        self.database = database if database else AppConfigs.INSTANCE['firebase.database']
        self.project_uuid = project_uuid if project_uuid else AppConfigs.INSTANCE['firebase.project.uuid']
        self.username = username if username else AppConfigs.INSTANCE['firebase.username']
        self.passphrase = passphrase if passphrase else AppConfigs.INSTANCE['firebase.passphrase']
        check_state(self.project_id, "Project ID must be defined")
        check_state(self.database, "Database name must be defined")
        check_state(self.username, "Username must be defined")
        self.set_passphrase()
        self.project_uuid = str(self.project_uuid) if self.project_uuid else str(uuid.uuid4())
        check_state(self.validate_config(), "Your Firebase configuration is not valid")
        log.debug("Successfully connected to Firebase: %s", self.base_url())

    def __str__(self):
        return self.CONFIG_FORMAT.format(
            self.project_id,
            self.username,
            self.database,
            str(base64.b64encode(self.passphrase.encode(self.encoding)), encoding=self.encoding),
            self.project_uuid
        )

    def set_passphrase(self) -> None:
        """TODO"""
        check_state(
            self.passphrase and len(self.passphrase) >= 8,
            "Passphrase must be have least 8 characters size and must be base64 encoded")
        self.passphrase = str(base64.b64decode(self.passphrase), encoding=self.encoding)

    def validate_config(self) -> bool:
        """TODO"""
        response = get('{}.json'.format(self.base_url()))
        is_valid = response is not None and response.status_code == HttpCode.OK
        if is_valid:
            self.current_state = response.body if response.body and response.body != 'null' else None
        return is_valid

    def base_url(self) -> str:
        """TODO"""
        return 'https://{}.firebaseio.com/{}/{}' \
            .format(self.project_id, self.database, self.project_uuid)

    def url(self, db_alias: str) -> str:
        """TODO"""
        return '{}/{}.json'.format(self.base_url(), db_alias)
