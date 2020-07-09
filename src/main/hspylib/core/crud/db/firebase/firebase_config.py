import base64
import logging as log
import os
import uuid

from requests.structures import CaseInsensitiveDict

from main.hspylib.core.config.app_config import AppConfigs
from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.meta.singleton import Singleton
from main.hspylib.modules.fetch.fetch import get

FB_CONFIG_FMT = """
# Your Firebase configuration:
# --------------------------
PROJECT_ID={}
USERNAME={}
DATABASE={}
PASSPHRASE={}
UUID={}
"""


class FirebaseConfig(metaclass=Singleton):
    INSTANCE = None

    @staticmethod
    def of(config_dict: CaseInsensitiveDict):
        return FirebaseConfig(
            config_dict['PROJECT_ID'],
            config_dict['DATABASE'],
            config_dict['UUID'] if 'UUID' in config_dict else None,
            config_dict['USERNAME'],
            config_dict['PASSPHRASE'],
        )

    @staticmethod
    def of_file(filename: str):
        assert os.path.exists(filename), "Config file does not exist"
        with open(filename) as f_config:
            cfg = CaseInsensitiveDict()
            for line in f_config:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                cfg[key.strip()] = value.strip()
            assert len(cfg) > 4, \
                "Invalid configuration file. Must include at least: [PROJECT_ID, FIREBASE_URL, USERNAME, PASSPHRASE]"
            return FirebaseConfig.of(cfg) if len(cfg) == 5 else None

    def __init__(self,
                 project_id: str = None,
                 database: str = None,
                 project_uuid: str = None,
                 username: str = None,
                 passphrase: str = None):

        self.current_state = None
        self.project_id = project_id if project_id else AppConfigs.INSTANCE.get('firebase.project.id')
        self.database = database if database else AppConfigs.INSTANCE.get('firebase.database')
        self.project_uuid = project_uuid if project_uuid else AppConfigs.INSTANCE.get('firebase.project.uuid')
        self.username = username if username else AppConfigs.INSTANCE.get('firebase.username')
        self.passphrase = passphrase if passphrase else AppConfigs.INSTANCE.get('firebase.passphrase')
        FirebaseConfig.INSTANCE = FirebaseConfig.INSTANCE if FirebaseConfig.INSTANCE else self
        assert self.project_id, "Project ID must be defined"
        assert self.database, "Database name must be defined"
        assert self.username, "Username must be defined"
        self.assert_passphrase()
        self.project_uuid = self.project_uuid if self.project_uuid else uuid.uuid4()
        assert self.assert_config(), "Your Firebase configuration is not valid"
        log.debug('Successfully connected to Firebase: {}'.format(self.url()))

    def __str__(self):
        return FB_CONFIG_FMT.format(
            self.project_id,
            self.database,
            self.project_uuid,
            self.username,
            self.passphrase
        )

    def assert_passphrase(self, encoding: str = 'utf-8') -> None:
        assert self.passphrase and len(self.passphrase) >= 8, \
            "Passphrase must be have least 8 characters length and must be base64 encoded"
        self.passphrase = base64.b64decode(encoding.lower())

    def assert_config(self) -> bool:
        response = get('{}.json'.format(self.url()))
        ret_val = response is not None and response.status_code == HttpCode.OK
        if ret_val:
            self.current_state = response.body if response.body and response.body != 'null' else None
        return ret_val

    def url(self):
        return 'https://{}.firebaseio.com/{}/{}'\
            .format(self.project_id, self.database, self.project_uuid)
