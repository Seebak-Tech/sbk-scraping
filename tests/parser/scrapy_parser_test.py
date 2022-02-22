import pytest
from pydantic import ValidationError
from sbk_scraping.parser.scrapy_parser import (
    HtmlXmlParser,
    SelectorParser,
    HtmlXmlSelectorParser,
    HtmlXmlParserFactory
)
from sbk_scraping.utils import get_logger


logger = get_logger(__name__)

data_body_html = '<html><body><span>good</span></body></html>'

srch_expr_dummy = {
    "target_id": "precio",
    "expr_type": 'xpath',
    "srchex": "//span/text()"
}

task_to_try = [
    ([{}], r".*This field is mandatory*", data_body_html),
    ([], r".*The list should have at least*", data_body_html),
    (srch_expr_dummy, r".*This field is not a valid list*", data_body_html),
    ([None], r".*None is not an allowed*", data_body_html)
]

task_ids = [
    "Invalid list elements",
    "Invalid number of elements in the list",
    "Invalid data type for srch_list_expressions",
    "Invalid None for list elements"
]


@pytest.mark.parametrize(
    'srch_lst_expr, match_msg, html_document',
    task_to_try,
    ids=task_ids
)
def test_validation_error_messages(srch_lst_expr, match_msg, html_document):
    with pytest.raises(
            ValidationError,
            match=match_msg
    ):
        parser = HtmlXmlParserFactory(
            srch_list_expressions=srch_lst_expr
        )
        _ = parser.parse(data=html_document)


@pytest.fixture()
def srch_lst_expressions():
    return [
        {
            "target_id": "title",
            "expr_type": "xpath",
            "srchex": "//*[@id=\"content_inner\"]/article//h1/text()"
        },
        {
            "target_id": "price",
            "expr_type": "xpath",
            "srchex": "//p[@class=\"price_color\"]/text()"
        },
        {
            "target_id": "non-existent",
            "expr_type": "css",
            "srchex": "span::text"
        }
    ]


def test_parse(html_str, srch_lst_expressions):
    expected = {
        "title": ['A Light in the Attic'],
        "price": ['£51.77']
    }
    html_parser = HtmlXmlParserFactory(
        srch_list_expressions=srch_lst_expressions
    )
    result = html_parser.parse(data=html_str)
    assert expected == result


def test_parse_properties(html_str, srch_lst_expressions):
    instance = HtmlXmlParserFactory(
        srch_list_expressions=srch_lst_expressions
    )
    result = instance.parse(data=html_str)
    assert len(result.keys()) <= len(instance.srch_list_expressions)


def test_regex_parser(html_str, srch_lst_expressions):
    regex = r'\d+'
    expected = {'price': ['51', '77']}
    result = HtmlXmlParserFactory(
        srch_list_expressions=srch_lst_expressions,
        regex=regex
    ).parse(data=html_str)
    print(result)
    assert result == expected


def test_invalid_regex_parser(html_str, srch_lst_expressions):
    match_msg = 'regular expression is invalid'
    regex = 'hell(o'
    with pytest.raises(
            ValidationError,
            match=match_msg
    ):
        _ = HtmlXmlParserFactory(
            srch_list_expressions=srch_lst_expressions,
            regex=regex
        ).parse(data=html_str)
