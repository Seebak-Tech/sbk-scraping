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
    "target_id": "non-existent",
    "srchex": "span.dummy"
}


@pytest.fixture()
def lst_expressions():
    return [
        {
            "target_id": "foo",
            "srchex": "foo.bar"
        },
        {
            "target_id": "first_name",
            "srchex": "people[?last=='f'].first"
        },
        {
            "target_id": "non-existent",
            "srchex": "span"
        }
    ]


def test_json_parser(lst_expressions):
    expected = {
        "first_name": ["Jayden"],
        "foo": "baz"
    }

    json_parser = JsonParser(srch_list_expressions=lst_expressions)

    result = json_parser.parse(data=json_data)
    assert result == expected


searches_to_try = [
    ([{}], r".*This field is mandatory*"),
    ([], r".*The list should have at least*"),
    (srch_expr_dict, r".*This field is not a valid list*"),
    ([None], r".*None is not an allowed*"),
]

test_ids = [
    "Invalid list elements",
    "Invalid number of elements in the list",
    "Invalid data type for srch_list_expressions",
    "Invalid None for list elements",
]


@pytest.mark.parametrize(
    'srch_lst_expr, match_msg',
    searches_to_try,
    ids=test_ids
)
def test_validation_errors(srch_lst_expr, match_msg):
    with pytest.raises(
            ValidationError,
            match=match_msg
    ):
        _ = JsonParser(srch_list_expressions=srch_lst_expr)


@given(expr_list=srch_expr_list_st())
def test_correct_initialization(expr_list):
    instance = JsonParser(srch_list_expressions=expr_list)
    for idx, srch_expr in enumerate(instance.srch_list_expressions):
        assert srch_expr.target_id == expr_list[idx]['target_id']
        assert srch_expr.srchex == expr_list[idx]['srchex']

    assert 0 < len(instance.srch_list_expressions)


@given(json_document=json_document_st(), expr_list=srch_expr_list_st())
def test_parse_properties(json_document, expr_list):
    instance = JsonParser(srch_list_expressions=expr_list)
    result = instance.parse(data=json_document)
    assert len(result.keys()) <= len(instance.srch_list_expressions)
