import pytest
from sbk_scraping.parser.factories import ParserFactory, InvalidValue
from sbk_scraping.parser.scrapy_parser import HtmlXmlParser
from sbk_scraping.parser.dynamic.json_parser import JsonParser


htmlxml_parser_id = "First"
json_parser_id = "Second"
wrong_parser_type = "Third"
wrong_parser_id = "wrong id"

validations_to_try = [
    (wrong_parser_id, r".*has invalid parser_id*"),
    (wrong_parser_type, r".*has invalid parser_type*"),
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


correct_validations_to_try = [
    (htmlxml_parser_id, HtmlXmlParser),
    (json_parser_id, JsonParser),
]

correct_validation_ids = [
    "The parser is an instance of HtmlXmlParser",
    "The parser_type is an instance of JsonParser",
]


@pytest.mark.parametrize(
    'parser_id_valid, parser',
    correct_validations_to_try,
    ids=correct_validation_ids
)
def test_parser(html_str, parser_id_valid, parser):
    parse = ParserFactory(
        data=html_str,
        parser_id=parser_id_valid,
    )
    instance = parse.build()
    assert isinstance(instance, parser)
