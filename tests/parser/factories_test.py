import pytest
from sbk_scraping.parser.scrapy_parser import HtmlXmlParser
from sbk_scraping.parser.dynamic.json_parser import JsonParser
from sbk_scraping.parser.factories import ParserFactory
from sbk_scraping.parser.common import InvalidValue
import sbk_scraping.constants as cnst
from sbk_scraping.utils import load_config_file


tasks_to_try = [
    ('html_str', "First", HtmlXmlParser),
    ('json_data', "Second", JsonParser),
]

tasks_ids = [
    "Valid HtmlXmlParser instance",
    "Valid JsonParser instance",
]


@pytest.mark.parametrize(
    'data, parser_id, parser_type',
    tasks_to_try,
    ids=tasks_ids
)
def test_build_parser(data,
                      parser_id,
                      parser_type,
                      request):
    parsers_config = load_config_file(file_name=cnst.PARSER_FILE_NAME)
    factory = ParserFactory.build_from_config(parsers_config)
    parser = factory.build_parser(
        data=request.getfixturevalue(data),
        parser_id=parser_id,
    )
    assert isinstance(parser, parser_type)


def test_invalid_parser_type(parsers_config, json_data):
    factory = ParserFactory.build_from_config(parsers_config)
    with pytest.raises(
            InvalidValue,
            match=r".*has invalid parser_type*"):

        _ = factory.build_parser(data=json_data, parser_id="Third")
