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
import base64
import getpass
import logging as log
import os
from typing import Optional

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.crud.db.firebase.firebase_config import FirebaseConfig
from hspylib.core.enums.charset import Charset
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import file_is_not_empty, sysout
from requests.structures import CaseInsensitiveDict

from firebase.core.firebase_auth import FirebaseAuth


class AgentConfig(metaclass=Singleton):
    """Holds the firebase agent configurations"""

    def __init__(self) -> None:
        self.app_configs = AppConfigs.INSTANCE
        self.firebase_configs = None
        if file_is_not_empty(self.config_file()):
            self.load()
            log.debug('Found and loaded a Firebase configuration: %s', self)

    def __str__(self) -> str:
        return str(self.firebase_configs)

    def __repr__(self):
        return str(self)

    def setup(self, config_dict: CaseInsensitiveDict) -> None:
        """Setup firebase from a dict configuration
        :param config_dict: Firebase configuration dictionary
        """
        config_dict['UID'] = FirebaseAuth.authenticate(config_dict).uid
        self.firebase_configs = FirebaseConfig.of(config_dict)
        self.save()

    def load(self) -> None:
        """Load configuration from file"""
        self.firebase_configs = FirebaseConfig.of_file(self.config_file())

    def prompt(self) -> None:
        """Create a new firebase configuration by prompting the user for information"""
        config = CaseInsensitiveDict()
        sysout("### Firebase setup")
        sysout('-' * 31)
        config['PROJECT_ID'] = self.project_id()
        config['DATABASE'] = self.database()
        config['EMAIL'] = self.email()
        config['PASSPHRASE'] = self.passphrase()
        self.setup(config)

    def config_file(self) -> str:
        """Return the configuration file"""
        file = self.app_configs['hhs.firebase.config.file']
        return file if file else f"{os.getenv('HOME', os.getcwd())}/.firebase"

    def project_id(self) -> Optional[str]:
        """Return the firebase project ID"""
        project_id = self.app_configs['hhs.firebase.project.id']
        return project_id if project_id else input('Please type you project ID: ')

    def database(self) -> Optional[str]:
        """Return the firebase project database name"""
        database = self.app_configs['hhs.firebase.database']
        return database if database else input('Please type you database Name: ')

    def email(self) -> Optional[str]:
        """Return the firebase username"""
        user = self.app_configs['hhs.firebase.email']
        return user if user else os.getenv('USER', f"{getpass.getuser()}@gmail.com")

    def passphrase(self) -> Optional[str]:
        """Return the firebase user passphrase"""
        passphrase = self.app_configs['hhs.firebase.passphrase']
        return passphrase if passphrase else self._input_passphrase()

    def url(self, db_alias: str) -> str:
        """Return the firebase project URL"""
        final_alias = db_alias.replace('.', '/')
        return self.firebase_configs.url(f'{final_alias}')

    def save(self) -> None:
        """Save current firebase configuration"""
        with open(self.config_file(), 'w+', encoding='utf-8') as f_config:
            f_config.write(str(self))
            sysout(f"Firebase configuration saved => {self.config_file()} !")

    def _input_passphrase(self) -> str:
        passwd = getpass.getpass('Please type a password to encrypt your data: ')
        return str(base64.b64encode(f"{self.email()}:{passwd}".encode(str(Charset.UTF_8))), str(Charset.UTF_8))
