import pytest
from pathlib import Path
from sbk_scraping.utils import ensure_path_exists, load_config_file


def test_ensure_path_exists():
    invalid_path = Path('/otro')
    with pytest.raises(
            ValueError,
            match='Validate the following'
    ):
        _ = ensure_path_exists(invalid_path)


def test_load_file():
    data = load_config_file('parsers.json')
    assert isinstance(data, dict)
