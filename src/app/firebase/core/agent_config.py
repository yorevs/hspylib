import base64
import getpass
import uuid
from logging import log
from typing import Any

from requests.structures import CaseInsensitiveDict

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.crud.db.firebase.firebase_config import FirebaseConfig
from hspylib.core.enum.charset import Charset
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout


class AgentConfig(metaclass=Singleton):

    def __init__(self):
        self.configs = AppConfigs.INSTANCE
        self.fb_configs = None

    def __str__(self):
        return str(self.fb_configs)

    def setup(self, config_dict: CaseInsensitiveDict) -> None:
        """Setup firebase config from dictionary
        :param config_dict: TODO
        """
        self.fb_configs = FirebaseConfig.of(config_dict)
        self.__save()

    def load(self):
        self.fb_configs = FirebaseConfig.of_file(self.config_file())

    def prompt(self) -> Any:
        """Create a configuration by prompting the user for information"""
        config = CaseInsensitiveDict()
        sysout("### Firebase setup")
        sysout('-' * 31)
        config['PROJECT_ID'] = self.project_id()
        config['DATABASE'] = self.database()
        config['USERNAME'] = self.username()
        config['PASSPHRASE'] = self.passphrase()
        config['UUID'] = self.uuid()
        self.setup(config)

    def logger(self) -> log:
        return self.configs.logger()

    def config_file(self) -> str:
        file = self.configs.get('firebase.config.file')
        return file if file else '{}/.firebase'.format(self.configs.resource_dir())

    def project_id(self):
        project_id = self.configs.get('firebase.project.id')
        return project_id if project_id else input('Please type you project ID: ')

    def database(self):
        database = self.configs.get('firebase.database')
        return database if database else input('Please type you database Name: ')

    def username(self) -> str:
        user = self.configs.get('firebase.username')
        return user if user else getpass.getuser()

    def passphrase(self):
        passphrase = self.configs.get('firebase.passphrase')
        return passphrase if passphrase else base64.b32encode(
            '{}:{}'.format(
                self.username(),
                getpass.getpass('Please type a password to encrypt your data: ')
            ).encode(str(Charset.UTF_8))
        )

    def uuid(self):
        project_uuid = self.configs.get('firebase.project.uuid')
        if not project_uuid:
            project_uuid = input('Please type a UUID to use or press [Enter] to generate a new one: ')
            project_uuid = str(uuid.uuid4()) if not project_uuid else project_uuid
        return project_uuid

    def url(self, db_alias: str) -> str:
        return self.fb_configs.url(db_alias)

    def __save(self) -> None:
        with open(self.config_file(), 'w') as f_config:
            f_config.write(str(self))
            AppConfigs.INSTANCE.logger().info("Firebase configuration saved !")
