from sbk_scraping.config import AppConfig
import pytest
import environ
import os


def test_invalid_configuration():
    with pytest.raises(ValueError, match='contains an invalid Path'):
        _ = environ.to_config(
            AppConfig,
            environ={"APP_ROOTDIR": "/work"}
        )


def test_config():
    config = environ.to_config(AppConfig)
    env_var = os.environ.get(
        "APP_ROOTDIR",
        '/workspace/sbk-scraping'
    ) + "/tests/test_data"

    assert env_var == str(config.testdata)
