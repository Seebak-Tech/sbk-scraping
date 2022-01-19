import json
import yaml
from pathlib import Path
from json.decoder import JSONDecodeError
from yaml.scanner import ScannerError
from yaml.parser import ParserError


def ensure_path_exists(path: Path):
    msg = f'\n*Cause: The Path does not exists'\
        f'\n*Action: Validate the following Path exists: ({path})'
    if not path.exists():
        raise ValueError(msg)


class InvalidSyntaxFile(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


def get_workdir() -> Path:
    from sbk_scraping.config import AppConfig
    import environ

    config = environ.to_config(AppConfig)
    path = config.rootdir

    if config.env.name == 'TEST':
        path = config.testdata
    return path


def load_json_file(path: Path) -> dict:
    ensure_path_exists(path)
    try:
        with path.open() as file:
            data = json.load(file)
        return data
    except JSONDecodeError:
        msg = '\n*Cause: The json file has invalid content'\
            '\n*Action: Validate that the json file is correct'
        raise InvalidSyntaxFile(msg)


def load_yaml_file(path: Path) -> dict:
    ensure_path_exists(path)
    try:
        with path.open() as file:
            data = yaml.safe_load(file)
        return data
    except (ScannerError, ParserError):
        msg = f'\n*Cause: YAML file has a syntax error in ({path})'\
            '\n*Action: Validate that the yaml file is correct'
        raise InvalidSyntaxFile(msg)


def load_parsers() -> dict:
    workdir = get_workdir()
    return load_json_file(workdir/'parsers.json')


def load_logger_config() -> dict:
    workdir = get_workdir()
    return load_yaml_file(workdir/'logging_config.yaml')
