import pytest
from sbk_scraping.parser.scrapy_parser import HtmlXmlParser
from sbk_scraping.parser.dynamic.json_parser import JsonParser
from sbk_scraping.parser.factories import ParserFactory
import sbk_scraping.constants as cnst
from sbk_scraping.utils import load_config_file


tasks_to_try = [
    ("First", HtmlXmlParser),
    ("Second", JsonParser),
]

tasks_ids = [
    "Valid HtmlXmlParser instance",
    "Valid JsonParser instance",
]


@pytest.mark.parametrize(
    'parser_id, parser_type',
    tasks_to_try,
    ids=tasks_ids
)
def test_build_parser(parser_id, parser_type):
    parsers_config = load_config_file(file_name=cnst.PARSER_FILE_NAME)
    factory = ParserFactory.build_from_config(parsers_config)
    parser = factory.build_parser(
        parser_id=parser_id,
    )
    assert isinstance(parser, parser_type)


def test_invalid_parser_type(parsers_config):
    factory = ParserFactory.build_from_config(parsers_config)
    with pytest.raises(
            ValueError,
            match=r".*has invalid parser_type*"):

        _ = factory.build_parser(parser_id="Third")


def test_parser_factory_set_srchex():
    expected_srchex = '//*[@id=\"content_inner\"]/article//h1/text()'

    factory = ParserFactory.build_from_config(
        config_dict=load_config_file(file_name=cnst.PARSER_FILE_NAME)
    )

    factory.set_srchex(
        parser_id='First',
        target_id='title',
        srchex='//*[@id=\"{}\"]/article//h1/text()'.format('content_inner')
    )

    assert expected_srchex == factory.get_srchex(
        parser_id='First',
        target_id='title'
    )


params_to_try = [
    ("First", 'html_str'),
    ("Second", 'json_data'),
]

params_ids = [
    "Valid HtmlXmlParser instance",
    "Valid JsonParser instance",
]


@pytest.mark.parametrize(
    'parser_id, data',
    params_to_try,
    ids=params_ids
)
def test_parse_parser(parser_id, data, request):
    body = str(request.getfixturevalue(data))
    parsers_config = load_config_file(file_name=cnst.PARSER_FILE_NAME)
    factory = ParserFactory.build_from_config(parsers_config)
    parser = factory.build_parser(parser_id=parser_id)
    result = parser.parse(data=body)
    assert isinstance(result, dict)
