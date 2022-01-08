import pytest
import environ
from sbk_scraping.config import AppConfig
from pathlib import Path


@pytest.fixture()
def test_data():
    config = environ.to_config(AppConfig)
    path = Path(config.testdata)
    return path


@pytest.fixture()
def valid_path():
    config = environ.to_config(AppConfig)
    path = Path(config.testdata/'srch_expressions.json')
    return path
