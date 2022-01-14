import pytest
from sbk_scraping.parser.factories import (
    ParserFactory,
    InvalidParseId,
    InvalidParserType
)


def test_parser_htmlxml_type(html_str):
    parse = ParserFactory(data=html_str, parser_id="First")
    result = parse.build()
    print(result)


def test_invalid_parser_id(html_str):
    with pytest.raises(
        InvalidParseId,
        match='has invalid parser id'
    ):
        parse = ParserFactory(data=html_str, parser_id="wrong id")
        _ = parse.build()


def test_invalid_parser_type(html_str):
    with pytest.raises(
        InvalidParserType,
        match='has invalid parser type'
    ):
        parse = ParserFactory(data=html_str, parser_id="Third")
        _ = parse.build()
