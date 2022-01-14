import pytest
from hypothesis import given, strategies as st
from pydantic import ValidationError
from sbk_scraping.parser.dynamic.json_parser import JsonParser
from tests.parser.common_test import (
    srch_expr_list_st,
    printable_text_st
)


def json_document_st(text_st=printable_text_st()):
    json_st = st.recursive(
        base=st.dictionaries(
                keys=text_st,
                values=(
                    text_st |
                    st.booleans() |
                    st.integers(min_value=1)
                ),
                min_size=1
        ),
        extend=lambda children: (
            st.dictionaries(keys=text_st, values=children, min_size=1)
        ),
        max_leaves=3
    )
    return json_st


json_data = {
    "people": [
        {"first": "James", "last": "d"},
        {"first": "Jacob", "last": "e"},
        {"first": "Jayden", "last": "f"},
        {"missing": "different"}
    ],
    "foo": {"bar": "baz"}
}

srch_expr_dict = {
    "target_field": "non-existent",
    "srch_expression": "span.dummy"
}


@pytest.fixture()
def lst_expressions():
    return [
        {
            "target_field": "foo",
            "srch_expression": "foo.bar"
        },
        {
            "target_field": "first_name",
            "srch_expression": "people[?last=='f'].first"
        },
        {
            "target_field": "non-existent",
            "srch_expression": "span"
        }
    ]


def test_jmes_parse(lst_expressions):
    expected = {
        "first_name": ["Jayden"],
        "foo": "baz"
    }

    json_parser = JsonParser(
        json_document=json_data,
        srch_list_expressions=lst_expressions
    )

    result = json_parser.parse()
    assert result == expected


searches_to_try = [
    (json_data, [{}], r".*This field is mandatory*"),
    (json_data, [], r".*The list should have at least*"),
    (None, [srch_expr_dict], r".*None is not an allowed*"),
    (json_data, srch_expr_dict, r".*This field is not a valid list*"),
    (json_data, [None], r".*None is not an allowed*"),
    (str(' '), [srch_expr_dict], r".*is not a valid dict*"),
]

test_ids = [
    "Invalid list elements",
    "Invalid number of elements in the list",
    "Invalid None for data_body",
    "Invalid data type for srch_list_expressions",
    "Invalid None for list elements",
    "Invalid json_data type",
]


@pytest.mark.parametrize(
    'json_document, srch_lst_expr, match_msg',
    searches_to_try,
    ids=test_ids
)
def test_validation_errors(json_document, srch_lst_expr, match_msg):
    with pytest.raises(
            ValidationError,
            match=match_msg
    ):
        _ = JsonParser(
            json_document=json_document,
            srch_list_expressions=srch_lst_expr
        )


@given(json_document=json_document_st(), expr_list=srch_expr_list_st())
def test_correct_initialization(json_document, expr_list):
    instance = JsonParser(
        json_document=json_document,
        srch_list_expressions=expr_list
    )
    for idx, srch_expr in enumerate(instance.srch_list_expressions):
        assert srch_expr.target_field == expr_list[idx]['target_field']
        assert srch_expr.srch_expression == expr_list[idx]['srch_expression']

    assert 0 < len(instance.srch_list_expressions)
    assert bool(instance.json_document)


@given(json_document=json_document_st(), expr_list=srch_expr_list_st())
def test_parse_properties(json_document, expr_list):
    instance = JsonParser(
        json_document=json_document,
        srch_list_expressions=expr_list
    )
    result = instance.parse()
    assert len(result.keys()) <= len(instance.srch_list_expressions)
