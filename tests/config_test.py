from sbk_scraping.config import AppConfig, ParserConfig
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
        '/workspace'
    ) + "/" + os.environ.get(
        "SBK_PROJECTNAME",
        'sbk-scraping'
    ) + "/" + "tests/test_data"

    assert env_var == str(config.testdata)


def test_get_parser_by_id(parsers_config, parser_dict):
    parser_conf = ParserConfig(parsers_config)
    assert parser_dict == parser_conf.get_parser_config(parser_id="First")


def test_get_srchex(parsers_config):
    srchex_expected = '//p[@class=\"price_color\"]/text()'
    parser_conf = ParserConfig(parsers_config)

    assert srchex_expected == parser_conf.get_srchex(
        parser_id='First',
        target_id='price'
    )


def test_set_srchex(parsers_config):
    expected_srchex = '//*[@id=\"content_inner\"]/article//h1/text()'

    parser_config = ParserConfig(parsers_config)
    parser_config.set_srchex(
        parser_id='First',
        target_id='title',
        srchex='//*[@id=\"{}\"]/article//h1/text()'.format('content_inner')
    )
    assert expected_srchex == parser_config.get_srchex(
        parser_id='First',
        target_id='title'
    )
#
#
#
#
#  def test_add_srch_expression(parsers_config):
#      assert False
