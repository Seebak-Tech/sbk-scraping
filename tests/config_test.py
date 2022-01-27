from hypothesis import given
from tests.parser.common_test import srch_expr_list_st
from sbk_scraping.config import AppConfig, ParserConfig, InvalidValue
import sbk_scraping.constants as cnst
from sbk_scraping.utils import load_config_file
import pytest
import environ
import os


def test_invalid_configuration():
    with pytest.raises(ValueError, match='contains an invalid Path'):
        _ = environ.to_config(
            AppConfig,
            environ={
                "SBK_WORKSPACE": "/work",
                "SBK_PROJECTNAME": "sbk-scraping"
            }
        )


def test_config():
    config = environ.to_config(AppConfig)
    env_var = os.environ.get(
        "SBK_WORKSPACE",
        cnst.DEFAULT_WORKSPACE
    ) + "/" + os.environ.get(
        "SBK_PROJECTNAME",
        cnst.PROJECT_NAME
    ) + "/" + cnst.TEST_DATA_PATH

    assert env_var == str(config.testdata)


config_to_try = [
    ({}, r".*The keys: \[('\w+')+\] should exists*"),
    (1, r".*The parsers configuration should be an a dict*")
]

test_ids = [
    "Invalid keys from configuration dict",
    "Invalid data type"
]


@pytest.mark.parametrize(
    'config_data, match_msg',
    config_to_try,
    ids=test_ids
)
def test_init_validation_errors(config_data, match_msg):
    with pytest.raises(
            InvalidValue,
            match=match_msg):
        _ = ParserConfig(config_data)


def test_get_parser_config(parsers_config, parser_dict):
    parser_conf = ParserConfig(parsers_config)
    assert parser_dict == parser_conf.get_parser_config(parser_id="First")
    with pytest.raises(
            InvalidValue,
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
            InvalidValue,
            match=r".*Validate that both ids are correct*"):
        parser_conf.get_srchex(parser_id='First', target_id='invalid_id')
    with pytest.raises(
            InvalidValue,
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
            InvalidValue,
            match=r".*Validate that the parser_id is correct*"):

        parser_config.set_srchex(
            parser_id='invalid_id',
            target_id='title',
            srchex='//*[@id=\"{}\"]/article//h1/text()'
        )
    with pytest.raises(
            InvalidValue,
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
            **srch_expression
        )

    after_add_size = len(
        parser_config.
        get_parser_config(parser_id="First")
        [cnst.CONFIG_SRCH_LST_EXPR_KEY]
    )
    assert after_add_size == size + len(srch_list_expr)
