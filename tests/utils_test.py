import pytest
from pathlib import Path
from sbk_scraping.utils import (
    ensure_path_exists,
    load_json_file,
    load_srch_expressions
)


def test_ensure_path_exists():
    invalid_path = Path('/otro')
    with pytest.raises(
            ValueError,
            match='Validate the following'
    ):
        _ = ensure_path_exists(invalid_path)


def test_load_json_file(valid_path):
    data = load_json_file(valid_path)
    assert len(data) != 0
    assert isinstance(data, dict)


def test_load_srch_expressions(test_data):
    data = load_srch_expressions(test_data)
    assert len(data) != 0
    assert isinstance(data, list)

    
