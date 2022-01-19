import pytest
from sbk_scraping.parser.scrapy_parser import HtmlXmlParser
from sbk_scraping.parser.dynamic.json_parser import JsonParser
from sbk_scraping.parser.factories import ParserFactory, InvalidValue


htmlxml_parser_id = "First"
json_parser_id = "Second"
invalid_parser_typ_id = "Third"
invalid_parser_id = "Wrong ID"

validations_to_try = [
    (invalid_parser_id, r".*has invalid parser_id*"),
    (invalid_parser_typ_id, r".*has invalid parser_type*"),
]

validation_ids = [
    "The parser_id is invalid",
    "The parser_type is invalid",
]


@pytest.mark.parametrize(
    'parser_id, match_msg',
    validations_to_try,
    ids=validation_ids
)
def test_invalid_parser_values(html_str, parser_id, match_msg):
    with pytest.raises(
        InvalidValue,
        match=match_msg
    ):
        parse = ParserFactory(
            data=html_str,
            parser_id=parser_id,
        )
        _ = parse.build()


tasks_to_try = [
    ('html_str', htmlxml_parser_id, HtmlXmlParser),
    ('json_data', json_parser_id, JsonParser),
]

tasks_ids = [
    "Valid HtmlXmlParser instance",
    "Valid JsonParser instance",
]


@pytest.mark.parametrize(
    'data, valid_parser_id, parser',
    tasks_to_try,
    ids=tasks_ids
)
def test_build_parser(data, valid_parser_id, parser, request):
    parse = ParserFactory(
        data=request.getfixturevalue(data),
        parser_id=valid_parser_id,
    )
    instance = parse.build()
    assert isinstance(instance, parser)


def test_load_logger_config(html_str):
    parse = ParserFactory(
        data=html_str,
        parser_id='First',
    )
    parse.build()
    assert isinstance(instance, HtmlXmlParser)

