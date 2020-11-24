import ast
import base64
import json
import os
from datetime import datetime

from hspylib.core.config.app_config import AppConfigs


class FirebaseEntry:
    def __init__(self,
                 db_alias: str,
                 username: str,
                 contents: dict):
        self.db_alias = db_alias
        self.contents = contents
        self.last_update_user = username
        self.last_update_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.payoload = {
            'contents': self.contents,
            'lastUpdate': self.last_update_date,
            'lastUser': self.last_update_user
        }

    def __str__(self):
        return json.dumps(self.__dict__)

    def parse_payload(self, payload: str) -> bool:
        try:
            dict_entry = dict(ast.literal_eval(json.loads(payload)))
            for key, value in dict_entry.items():
                self.payoload[key] = value
            return True
        except ValueError:
            return False

    def load_all(self):
        for name, dotfile in self.contents.items():
            if os.path.exists(dotfile):
                AppConfigs.INSTANCE.logger().debug("Reading name={} dotfile={}".format(name, dotfile))
                with open(dotfile, 'r') as f_dotfile:
                    self.payoload[name] = str(base64.b64encode(f_dotfile.read()))
            else:
                AppConfigs.INSTANCE.logger().warn("Dotfile {} does not exist. Ignoring it".format(dotfile))

        return self

    def save_all(self):
        for name, dotfile in self.contents.items():
            if name in self.payoload:
                AppConfigs.INSTANCE.logger().debug("Saving name={} dotfile={}".format(name, dotfile))
                with open(dotfile, 'w') as f_dotfile:
                    f_dotfile.write(str(base64.b64decode(self.payoload[name])))
            else:
                AppConfigs.INSTANCE.logger().warn("Name={} is not part of data. Ignoring it".format(name))

        return self
