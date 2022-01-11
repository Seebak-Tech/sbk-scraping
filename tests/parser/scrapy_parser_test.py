import pytest
import environ
from pydantic import ValidationError
from sbk_scraping.parser.scrapy_parser import HtmlXmlParser
from sbk_scraping.config import AppConfig


data_body_html = '<html><body><span>good</span></body></html>'

srch_expr_dummy = {
    "target_field": "precio",
    "expr_type": 'xpath',
    "srch_expression": "//span/text()"
}

task_to_try = [
    (data_body_html, [{}], r".*This field is mandatory*"),
    ('', [srch_expr_dummy], r".*This field should contain at least 1 charac*"),
    (data_body_html, [], r".*The list should have at least*"),
    (None, [srch_expr_dummy], r".*None is not an allowed*"),
    (data_body_html, srch_expr_dummy, r".*This field is not a valid list*"),
    (data_body_html, [None], r".*None is not an allowed*"),
    ({}, [srch_expr_dummy], r".*This field should be a string*"),
]

task_ids = [
    "Invalid list elements",
    "Invalid html str",
    "Invalid number of elements in the list",
    "Invalid None for data_body",
    "Invalid data type for srch_list_expressions",
    "Invalid None for list elements",
    "Invalid data_body type",
]


@pytest.mark.parametrize(
    'html_document, srch_lst_expr, match_msg',
    task_to_try,
    ids=task_ids
)
def test_validation_error_messages(html_document, srch_lst_expr, match_msg):
    with pytest.raises(
            ValidationError,
            match=match_msg
    ):
        _ = HtmlXmlParser(
            data_body=html_document,
            srch_list_expressions=srch_lst_expr
        )


@pytest.fixture()
def html_str(test_data):
    with open(test_data/'book_to_scrape.html') as body_file:
        body_data = body_file.read()
    return body_data


@pytest.fixture()
def srch_lst_expressions():
    return [
        {
            "target_field": "title",
            "expr_type": "xpath",
            "srch_expression": "//*[@id=\"content_inner\"]/article//h1/text()"
        },
        {
            "target_field": "price",
            "expr_type": "xpath",
            "srch_expression": "//p[@class=\"price_color\"]/text()"
        },
        {
            "target_field": "non-existent",
            "expr_type": "css",
            "srch_expression": "span::text"
        }
    ]


@pytest.fixture()
def srch_lst_expressions_type():
    return [
        {
            "expr_type": "xpath",
        },
        {
            "expr_type": "css",
        }
    ]


def test_parse(html_str, srch_lst_expressions, srch_lst_expressions_type):
    expected = {
        "title": ['A Light in the Attic'],
        "price": ['£51.77']
    }
    html_parser = HtmlXmlParser(
        data_body=html_str,
        srch_list_expressions=srch_lst_expressions,
        #  srch_list_expr_type=srch_lst_expressions_type
    )
    result = html_parser.parse()
    assert expected == result


def test_parse_properties(html_str, srch_lst_expressions):
    instance = HtmlXmlParser(
        data_body=html_str,
        srch_list_expressions=srch_lst_expressions
    )
    result = instance.parse()
    assert len(result.keys()) <= len(instance.srch_list_expressions)
