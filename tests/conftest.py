import pytest
import environ
from sbk_scraping.config import AppConfig


@pytest.fixture(scope="session")
def config():
    return environ.to_config(AppConfig)


@pytest.fixture(scope="session")
def test_data(config):
    path = config.testdata
    return path
