import pytest
from sbk_scraping.parser.scrapy_parser import HtmlXmlParser
from sbk_scraping.parser.dynamic.json_parser import JsonParser
from sbk_scraping.parser.factories import ParserFactory
from sbk_scraping.parser.common import InvalidValue 


htmlxml_parser_id = "First"
json_parser_id = "Second"
invalid_parser_id = "Wrong ID"


tasks_to_try = [
    ('html_str', htmlxml_parser_id, HtmlXmlParser),
    ('json_data', json_parser_id, JsonParser),
]

tasks_ids = [
    "Valid HtmlXmlParser instance",
    "Valid JsonParser instance",
]


@pytest.mark.parametrize(
    'data, valid_parser_id, parser_type',
    tasks_to_try,
    ids=tasks_ids
)
def test_build_parser(parsers_config,
                      data,
                      valid_parser_id,
                      parser_type,
                      request):
    factory = ParserFactory.build_from_config(parsers_config)
    parser = factory.build_parser(
        data=request.getfixturevalue(data),
        parser_id=valid_parser_id,
    )
    assert isinstance(parser, parser_type)


def test_invalid_parser_type(parsers_config, json_data):
    factory = ParserFactory.build_from_config(parsers_config)
    with pytest.raises(
            InvalidValue,
            match=r".*has invalid parser_type*"):

        _ = factory.build_parser(data=json_data, parser_id="Third")
