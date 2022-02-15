import pytest
from sbk_scraping.parser.scrapy_parser import HtmlXmlParser
from sbk_scraping.parser.dynamic.json_parser import JsonParser
from sbk_scraping.parser.factories import ParserFactory, ParserConfig
from hypothesis import given
from tests.parser.common_test import srch_expr_list_st
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


config_to_try = [
    ({}, r".*The dictionary must contain all the following*", ValueError),
    (1, r".*The object must be type of *", TypeError)
]

test_ids = [
    "Invalid keys from configuration dict",
    "Invalid data type"
]


@pytest.mark.parametrize(
    'config_data, match_msg, error',
    config_to_try,
    ids=test_ids
)
def test_init_validation_errors(config_data, match_msg, error):
    with pytest.raises(
            error,
            match=match_msg):
        _ = ParserConfig(config_data)


def test_get_parser_config(parsers_config, parser_dict):
    parser_conf = ParserConfig(parsers_config)
    assert parser_dict == parser_conf.get_parser_config(parser_id="First")
    with pytest.raises(
            ValueError,
            match=r".*Validate that the parser_id is correct*"):

        parser_conf.get_parser_config(parser_id='invalid_parser_id')


def test_get_srchex(parsers_config):
    srchex_expected = '//p[@class=\"price_color\"]/text()'
    parser_conf = ParserConfig(parsers_config)

    assert srchex_expected == parser_conf.get_srchex(
        parser_id='First',
        target_id='price'
    )
    with pytest.raises(
            ValueError,
            match=r".*Validate that both ids are correct*"):
        parser_conf.get_srchex(parser_id='First', target_id='invalid_id')
    with pytest.raises(
            ValueError,
            match=r".*Validate that both ids are correct*"):
        parser_conf.get_srchex(parser_id='invalid_id', target_id='price')


def test_set_srchex():
    expected_srchex = '//*[@id=\"content_inner\"]/article//h1/text()'

    parsers_dict = load_config_file(file_name=cnst.PARSER_FILE_NAME)
    parser_config = ParserConfig(parsers_dict)
    parser_config.set_srchex(
        parser_id='First',
        target_id='title',
        srchex='//*[@id=\"{}\"]/article//h1/text()'.format('content_inner')
    )
    assert expected_srchex == parser_config.get_srchex(
        parser_id='First',
        target_id='title'
    )
    with pytest.raises(
            ValueError,
            match=r".*Validate that the parser_id is correct*"):

        parser_config.set_srchex(
            parser_id='invalid_id',
            target_id='title',
            srchex='//*[@id=\"{}\"]/article//h1/text()'
        )
    with pytest.raises(
            ValueError,
            match=r".*Validate that the target_id is correct*"):

        parser_config.set_srchex(
            parser_id='First',
            target_id='invalid_id',
            srchex='//*[@id=\"{}\"]/article//h1/text()'
        )


@given(srch_list_expr=srch_expr_list_st())
def test_add_srch_expression(srch_list_expr):
    parsers_dict = load_config_file(file_name=cnst.PARSER_FILE_NAME)
    parser_config = ParserConfig(parsers_dict)
    size = len(
        parser_config.
        get_parser_config(parser_id="First")
        [cnst.CONFIG_SRCH_LST_EXPR_KEY]
    )
    for srch_expression in srch_list_expr:
        parser_config.add_srch_expression(
            parser_id='First',
            srch_expr_dict=srch_expression
        )

    after_add_size = len(
        parser_config.
        get_parser_config(parser_id="First")
        [cnst.CONFIG_SRCH_LST_EXPR_KEY]
    )
    assert after_add_size == size + len(srch_list_expr)
