from hspylib.core.config.app_config import AppConfigs


class VaultOpenError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        AppConfigs.INSTANCE.logger().error(message)
