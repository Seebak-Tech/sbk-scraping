from sbk_scraping.config import AppConfig
import pytest
import environ


def test_invalid_configuration():
    with pytest.raises(ValueError, match='contains an invalid Path'):
        _ = environ.to_config(
            AppConfig,
            environ={"APP_ROOTDIR": "/work"}
        )


def test_config():
    config = environ.to_config(
        AppConfig,
        environ={"APP_ROOTDIR": "/workspace/sbk-scraping"}
    )
    assert "/workspace/sbk-scraping/tests/test_data" == str(config.testdata)
