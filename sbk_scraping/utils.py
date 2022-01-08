import json
from pathlib import Path


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


def load_srch_expressions(srch_expr_path: Path) -> dict:
    data = load_json_file(srch_expr_path/'srch_expressions.json')
    return data.get('srch_expressions', {})
