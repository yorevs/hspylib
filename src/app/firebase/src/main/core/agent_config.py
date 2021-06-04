#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.firebase.src.main.core
      @file: agent_config.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import base64
import getpass
import uuid

from requests.structures import CaseInsensitiveDict

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.crud.db.firebase.firebase_config import FirebaseConfig
from hspylib.core.enums.charset import Charset
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import sysout


class AgentConfig(metaclass=Singleton):
    """Holds the firebase agent configurations"""

    def __init__(self):
        self.configs = AppConfigs.INSTANCE
        self.fb_configs = None

    def __str__(self):
        return str(self.fb_configs)

    def __repr__(self):
        return str(self)

    def setup(self, config_dict: CaseInsensitiveDict) -> None:
        """Setup firebase from a dict configuration
        :param config_dict: Firebase configuration dictionary
        """
        self.fb_configs = FirebaseConfig.of(config_dict)
        self.save()

    def load(self) -> None:
        """Load configuration from file"""
        self.fb_configs = FirebaseConfig.of_file(self.config_file())

    def prompt(self) -> None:
        """Create a new firebase configuration by prompting the user for information"""
        config = CaseInsensitiveDict()
        sysout("### Firebase setup")
        sysout('-' * 31)
        config['PROJECT_ID'] = self.project_id()
        config['DATABASE'] = self.database()
        config['USERNAME'] = self.username()
        config['PASSPHRASE'] = self.passphrase()
        config['UUID'] = self.uuid()
        self.setup(config)

    def config_file(self) -> str:
        """Return the configuration file"""
        file = self.configs['firebase.config.file']
        return file if file else f"{self.configs.resource_dir()}/firebase.cfg"

    def project_id(self) -> str:
        """Return the firebase project ID"""
        project_id = self.configs['firebase.project.id']
        return project_id if project_id else input('Please type you project ID: ')

    def database(self) -> str:
        """Return the firebase project database name"""
        database = self.configs['firebase.database']
        return database if database else input('Please type you database Name: ')

    def username(self) -> str:
        """Return the firebase username"""
        user = self.configs['firebase.last_update_user']
        return user if user else getpass.getuser()

    def passphrase(self) -> str:
        """Return the firebase user passphrase"""
        passphrase = self.configs['firebase.passphrase']
        return passphrase if passphrase else base64.b32encode(
            '{}:{}'.format(
                self.username(),
                getpass.getpass('Please type a password to encrypt your data: ')
            ).encode(str(Charset.UTF_8))
        )

    def uuid(self) -> str:
        """Return the firebase project UUID or assign a new one if not speficied"""
        project_uuid = self.configs['firebase.project.uuid']
        if not project_uuid:
            project_uuid = input('Please type a UUID to use or press [Enter] to generate a new one: ')
            project_uuid = str(uuid.uuid4()) if not project_uuid else project_uuid
        return project_uuid

    def url(self, db_alias: str) -> str:
        """Return the firebase project URL"""
        return self.fb_configs.url(db_alias)

    def save(self) -> None:
        """Save current firebase configuration"""
        with open(self.config_file(), 'w') as f_config:
            f_config.write(str(self))
            AppConfigs.INSTANCE.logger().tooltip("Firebase configuration saved !")
