from sbk_scraping.config import AppConfig
import sbk_scraping.constants as cnst
import pytest
import environ
import os


def test_invalid_configuration():
    with pytest.raises(ValueError, match='contains an invalid Path'):
        _ = environ.to_config(
            AppConfig,
            environ={
                "SBK_WORKSPACE": "/work",
                "SBK_PROJECTNAME": "sbk-scraping"
            }
        )


def test_config():
    config = environ.to_config(AppConfig)
    env_var = os.environ.get(
        "SBK_WORKSPACE",
        cnst.DEFAULT_WORKSPACE
    ) + "/" + os.environ.get(
        "SBK_PROJECTNAME",
        cnst.PROJECT_NAME
    ) + "/" + cnst.TEST_DATA_PATH

    assert env_var == str(config.testdata)
