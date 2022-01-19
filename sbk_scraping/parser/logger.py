import logging.config
import logging
from sbk_scraping.utils import load_logger_config, load_enviroment


class SetUpLogging():
    def __init__(self):
        self.default_config = load_enviroment()/'logging_config.yaml'

    def setup_logging(self, default_level=logging.info):
        path = self.default_config
        if path.exists():
            config = load_logger_config()
            logging.config.dictConfig(config)
            logging.captureWarnings(True)
        else:
            logging.basicConfig(level=default_level)
