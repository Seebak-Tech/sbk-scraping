import pytest
from pathlib import Path
from sbk_scraping.utils import (
    ensure_path_exists,
    read_parsers
)


def test_ensure_path_exists():
    invalid_path = Path('/otro')
    with pytest.raises(
            ValueError,
            match='Validate the following'
    ):
        _ = ensure_path_exists(invalid_path)


def test_read_parsers(config):
    data = read_parsers(config)
    assert len(data) != 0
    assert isinstance(data, dict)
