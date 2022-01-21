import re
import pytest
from hypothesis import strategies as st
from pydantic import ValidationError
from sbk_scraping.parser.common import SrchTypeExpression


def printable_text_st():
    re_expression = re.compile(r"[a-zA-Z_]+")
    return st.from_regex(
        regex=re_expression,
        fullmatch=True
    )


def expr_type_st():
    return st.one_of(st.just('xpath'), st.just('css'))


def qry_expression_st(text_st=printable_text_st(), type_st=expr_type_st()):
    qry_expressions_st = st.fixed_dictionaries(
        mapping={
            'target_id': text_st,
            'srchex': text_st
        },
        optional={'expr_description': text_st,
                  'expr_type': type_st,
                  }
    )
    return qry_expressions_st


def srch_expr_list_st(qry_expressions=qry_expression_st()):
    return st.lists(qry_expressions, min_size=1)


srch_expr_wthout_trgt = {
    "expr_type": "xpath",
    "srchex": "//span/text()"
}

srch_expr_wthout_expr_typ = {
    "target_id": "precio",
    "srchex": "//span/text()"
}

srch_expr_wthout_expr = {
    "target_id": "precio",
    "expr_type": 'xpath',
}

srch_expr_invalid_expr_type = {
    "target_id": "precio",
    "expr_type": 'json',
    "srchex": "//span/text()"
}

validations_to_try = [
    (srch_expr_wthout_trgt, r".*This field is mandatory*"),
    (srch_expr_wthout_expr_typ, r".*This field is mandatory*"),
    (srch_expr_wthout_expr, r".*This field is mandatory*"),
    (srch_expr_invalid_expr_type, r".*The permitted values are*"),
]

validation_ids = [
    "Miss target_id",
    "Miss expr_type field",
    "Miss srch_expressions field",
    "Invalid expresion type",
]


@pytest.mark.parametrize(
    'srch_lst_expr, match_msg',
    validations_to_try,
    ids=validation_ids
)
def test_mandatory_fields(srch_lst_expr, match_msg):
    with pytest.raises(
            ValidationError,
            match=match_msg
    ):
        _ = SrchTypeExpression(**srch_lst_expr)
