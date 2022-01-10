import pytest
import environ
from sbk_scraping.config import AppConfig


@pytest.fixture(scope="session")
def config():
<<<<<<< HEAD
    return environ.to_config(AppConfig)
=======
    config = environ.to_config(
        AppConfig,
        environ={
            "SBK_ENV": "test"
        }
    )
    return config
>>>>>>> 866fb66701bff72e185abdb826f59250dd72f375


@pytest.fixture(scope="session")
def test_data(config):
    path = config.testdata
    return path
