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


@pytest.fixture(scope="session")
def html_str(test_data):
    with open(test_data/'book_to_scrape.html') as body_file:
        body_data = body_file.read()
    return body_data
