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


@pytest.fixture(scope="session")
def json_data(test_data):
    import json
    with open(test_data/'data.json') as body_file:
        body_data = json.load(body_file)
    return body_data


@pytest.fixture(scope="session", params=[html_str, json_data])
def data_file(request):
    return request.param
