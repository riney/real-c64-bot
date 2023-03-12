import json, logging, os

logger = logging.getLogger('config')
logging.basicConfig(level=logging.INFO)

class Config(object):
    _instance = None
    config = None

    CONFIG_FILE_NAME_ENV_VAR = "CONFIG"
    DEFAULT_CONFIG_FILE_NAME = "config.json"

    def __new__(cls):
        if cls._instance is None:
            logger.info('Creating config.')
            cls._instance = super(Config, cls).__new__(cls)
            config_file_name = os.environ.get(Config.CONFIG_FILE_NAME_ENV_VAR) or Config.DEFAULT_CONFIG_FILE_NAME

            logger.info(f"Loading config from {config_file_name}")
            with open(config_file_name) as f:
                cls._instance.config = json.load(f)

        return cls._instance

    def values(self):
        return self.config
