import json
from pathlib import Path
import environ
from sbk_scraping.config import AppConfig


def ensure_path_exists(path: Path):
    msg = f'\n*Cause: The Path does not exists'\
        f'\n*Action: Validate the following Path exists: ({path})'
    if not path.exists():
        raise ValueError(msg)


def load_json_file(path: Path) -> dict:
    ensure_path_exists(path)
    with path.open() as file:
        data = json.load(file)
    return data


def read_parsers(config) -> dict:
    path = config.rootdir
    if config.env.name == 'TEST':
        path = config.testdata
    data = load_json_file(path/'parsers.json')
    return data
