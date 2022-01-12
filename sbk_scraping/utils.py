import json
from pathlib import Path
from json.decoder import JSONDecodeError


def ensure_path_exists(path: Path):
    msg = f'\n*Cause: The Path does not exists'\
        f'\n*Action: Validate the following Path exists: ({path})'
    if not path.exists():
        raise ValueError(msg)


class InvalidJsonContent(Exception):
    def __init__(self, mensaje):
        Exception.__init__(self, mensaje)


def load_json_file(path: Path) -> dict:
    ensure_path_exists(path)
    try:
        with path.open() as file:
            data = json.load(file)
        return data
    except JSONDecodeError:
        msg = '\n*Cause: The json file has invalid content'\
            '\n*Action: Validate that the json file is correct'
        raise InvalidJsonContent(msg)


def read_parsers(config) -> dict:
    path = config.rootdir
    if config.env.name == 'TEST':
        path = config.testdata
    data = load_json_file(path/'parsers.json')
    return data
