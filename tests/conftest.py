import pytest
import environ
from sbk_scraping.config import AppConfig
from sbk_scraping.utils import load_parsers


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


@pytest.fixture(scope="session")
def parsers_config():
    return load_parsers()


@pytest.fixture(scope="session")
def parser_dict():
    return {
        "parser_type": "HtmlXml",
        "parser_id": "First",
        "srch_expressions": [
            {
              "target_id": "title",
              "expr_type": "xpath",
              "srchex": "//*[@id=\"{}\"]/article//h1/text()"
            },
            {
              "target_id": "price",
              "expr_type": "xpath",
              "srchex": "//p[@class=\"price_color\"]/text()"
            },
            {
              "target_id": "non-existent",
              "expr_type": "css",
              "srchex": "span::text"
            }
        ]
    }
