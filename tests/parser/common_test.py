import re
import pytest
from hypothesis import strategies as st
from pydantic import ValidationError
from sbk_scraping.parser.common import SearchExpression


def printable_text_st():
    re_expression = re.compile(r"[a-zA-Z_]+")
    return st.from_regex(
        regex=re_expression,
        fullmatch=True
    )


def qry_expression_st(text_st=printable_text_st()):
    qry_expressions_st = st.fixed_dictionaries(
        mapping={
            'target_field': text_st,
            'expr_type': text_st,
            'srch_expression': text_st
        },
        optional={'expr_description': text_st}
    )
    return qry_expressions_st


def srch_expr_list_st(qry_expressions=qry_expression_st()):
    return st.lists(qry_expressions, min_size=1)


@pytest.mark.parametrize(
    ('srch_expressions', 'match_expr'),
    (
        (
            {'target_field': 'names', 'expr_type': 'jmes'},
            r".*srch_expression*"
        ),
        (
            {'expr_type': 'jmes', 'srch_expression': 'people[*].first'},
            r".*target_field*"
        ),
        (
            {'target_field': 'name', 'srch_expression': 'people[*].first'},
            r".*expr_type*"
        ),
    ),
)
def test_mandatory_fields(srch_expressions, match_expr):
    with pytest.raises(
            ValidationError,
            match=match_expr
    ):
        _ = SearchExpression(**srch_expressions)
