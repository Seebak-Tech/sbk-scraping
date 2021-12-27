import pytest
from hypothesis import given, strategies as st
from pydantic import ValidationError
from sbk_scraping.parser.dynamic.json_parser import JmesPathParser
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
        max_leaves=5
    )
    return json_st


json_dict = {
    "people": [
        {"first": "James", "last": "d"},
        {"first": "Jacob", "last": "e"},
        {"first": "Jayden", "last": "f"},
        {"missing": "different"}
    ],
    "foo": {"bar": "baz"}
}

srch_expr_dict = {
    "target_field": "names",
    "expr_type": 'jmes',
    "srch_expression": "people[*].first"
}


@pytest.mark.parametrize(
    ('json_document', 'srch_lst_expressions', 'match_expr'),
    (
        ({}, [{}], r".*This field is mandatory"),
        (json_dict, [{}], r".*This field is mandatory"),
        (json_dict, [], r".*The list should have at least*"),
        (None, [srch_expr_dict], r".*None is not an allowed*"),
        (json_dict, srch_expr_dict, r".*This field is not a valid list*"),
    ),
)
def test_validation_errors(json_document, srch_lst_expressions, match_expr):
    with pytest.raises(
            ValidationError,
            match=match_expr
    ):
        _ = JmesPathParser(
            json_document=json_document,
            srch_list_expressions=srch_lst_expressions
        )


@given(json_document=json_document_st(), expr_list=srch_expr_list_st())
def test_correct_initialization(json_document, expr_list):
    instance = JmesPathParser(
        json_document=json_document,
        srch_list_expressions=expr_list
    )
    for idx, srch_expr in enumerate(instance.srch_list_expressions):
        assert srch_expr.target_field == expr_list[idx]['target_field']
        assert srch_expr.expr_type == expr_list[idx]['expr_type']
        assert srch_expr.srch_expression == expr_list[idx]['srch_expression']

    assert 0 < len(instance.srch_list_expressions)
    assert bool(instance.json_document)


@given(json_document=json_document_st(), expr_list=srch_expr_list_st())
def test_parse_object(json_document, expr_list):
    instance = JmesPathParser(
        json_document=json_document,
        srch_list_expressions=expr_list
    )
    result = instance.parse()
    assert len(result) <= len(instance.srch_list_expressions)
