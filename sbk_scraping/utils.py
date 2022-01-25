from pathlib import Path
from typing import Dict
from sbk_utils.io.loader import FileHandlerFactory


def ensure_path_exists(path: Path):
    msg = f'\n*Cause: The Path does not exists'\
        f'\n*Action: Validate the following Path exists: ({path})'
    if not path.exists():
        raise ValueError(msg)


def get_workdir() -> Path:
    from sbk_scraping.config import AppConfig
    import environ

    config = environ.to_config(AppConfig)
    path = config.rootdir

    if config.env.name == 'TEST':
        path = config.testdata
    return path


def load_config_file(file_name) -> Dict:
    workdir = get_workdir()
    file_handler = FileHandlerFactory.build_from_file(
        workdir/'config'/file_name
    )
    return file_handler.load()


def get_logger(logger_name: str):
    import logging.config
    import logging
    dict_config = load_config_file('logging_config.yaml')
    logging.config.dictConfig(dict_config)
    return logging.getLogger(logger_name)
