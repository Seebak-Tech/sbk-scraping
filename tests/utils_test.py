import pytest
from pathlib import Path
from sbk_scraping.utils import (
    ensure_path_exists,
    load_json_file,
    load_parsers,
    InvalidSyntaxFile,
    load_yaml_file,
    load_logger_config
)


def test_ensure_path_exists():
    invalid_path = Path('/otro')
    with pytest.raises(
            ValueError,
            match='Validate the following'
    ):
        _ = ensure_path_exists(invalid_path)


def test_load_parsers():
    data = load_parsers()
    assert len(data) != 0
    assert isinstance(data, dict)


def test_invalid_content_jsonfile(test_data):
    with pytest.raises(
        InvalidSyntaxFile,
        match='has invalid content'
    ):
        _ = load_json_file(test_data/"invalid_content.json")


def test_invalid_yaml_file(test_data):
    with pytest.raises(
        InvalidSyntaxFile,
        match=' has a syntax error in'
    ):
        _ = load_yaml_file(test_data/"book_to_scrape.html")


def test_load_logger_config():
    logger_config = load_logger_config()
    assert len(logger_config) != 0
    assert isinstance(logger_config, dict)
