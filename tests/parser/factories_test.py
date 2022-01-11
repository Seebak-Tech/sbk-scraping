import pytest
from sbk_scraping.parser.factories import ParserFactory


@pytest.fixture()
def valid_htmlxml_type():
    pass


@pytest.fixture()
def valid_json_type():
    pass


def test_parser_htmlxml_type(config):
    parse = ParserFactory()
    parse.parser_type(config)


def test_parser_json_type(config):
    pass
    

def test_valid_srch_expres():
    pass
