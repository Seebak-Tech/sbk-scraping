import pytest
import environ
from sbk_scraping.config import AppConfig


@pytest.fixture(scope="session")
def config():
    config = environ.to_config(
        AppConfig,
        environ={
            "SBK_ENV": "test"
        }
    )
    return config


@pytest.fixture(scope="session")
def test_data(config):
    path = config.testdata
    return path
