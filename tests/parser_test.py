import pytest
import warnings
import string
from hypothesis import given, strategies as st
from pydantic import ValidationError
from sbk_scraping.parser import (
    JmesPathParser,
    InvalidValue
)

warnings.filterwarnings("ignore", category=DeprecationWarning)


test_dict = {
    "people": [
        {"first": "James", "last": "d"},
        {"first": "Jacob", "last": "e"},
        {"first": "Jayden", "last": "f"},
        {"missing": "different"}
    ],
    "foo": {"bar": "baz"}
}


@pytest.mark.parametrize(
    ('json_document', 'srch_list_expressions'),
    (
        (
            '{"key": "value"}', {
                "expr_tag": "people names",
                "expression": 'people[*].first'
            }
        ),
        (test_dict, {'peple[*].first'}),
        (test_dict, 3),
    ),
)
def test_parameter_failure(json_document, srch_list_expressions):
    with pytest.raises(ValidationError):
        _ = JmesPathParser(
            json_document=json_document,
            srch_list_expressions=srch_list_expressions
        )


@pytest.mark.parametrize(
    ('json_document', 'srch_list_expressions'),
    (
        ({}, [{}]),
        ({}, [{'expr_tag': 'names', 'expression': 'people[*].first'}]),
        (test_dict, [{}]),
        (test_dict, [])
    ),
)
def test_zero_values(json_document, srch_list_expressions):
    with pytest.raises(InvalidValue):
        _ = JmesPathParser(
            json_document=json_document,
            srch_list_expressions=srch_list_expressions
        )


@pytest.mark.parametrize(
    ('json_document', 'json_expressions'),
    (
        (
            test_dict,
            [
                {'expr_tag': 'names', 'srch_expression': 'people[*].first'},
                {'expr_tag': 'last_names', 'srch_expression': 'people[*].last'}
            ],
        ),
        (
            test_dict,
            [{'expr_tag': 'last_names', 'srch_expression': 'people[*].last'}],
        )
    ),
)
def test_correct_initialization(json_document, json_expressions):
    result = JmesPathParser(
        json_document=json_document,
        srch_list_expressions=json_expressions
    )
    for index, qry_expression in enumerate(result.srch_list_expressions):
        result_expr_tag = qry_expression.expr_tag

        assert result_expr_tag == json_expressions[index]['expr_tag']

def printable_text_st():
    return st.text(
        alphabet=list(string.ascii_letters),
        min_size=4
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
        extend=lambda children:(
            st.dictionaries(keys=text_st, values=children, min_size=1)
        ),
        max_leaves=5
    )
    return json_st

def qry_expression_st(text_st=printable_text_st()):
    qry_expressions_st = st.fixed_dictionaries(
        mapping={'expr_tag': text_st, 'srch_expression': text_st},
        optional={'expr_description': text_st}
    )
    return qry_expressions_st

def qry_expr_list_st(qry_expressions=qry_expression_st()):
    return st.lists(qry_expressions, min_size=1)
    

@given(json_document=json_document_st(), qry_expr_list=qry_expr_list_st())
def test_instances(json_document, qry_expr_list):
    instance = JmesPathParser(
        json_document=json_document,
        srch_list_expressions=qry_expr_list
    )
    assert 0 < len(instance.srch_list_expressions)
    assert bool(instance.json_document)


@given(json_document=json_document_st(), qry_expr_list=qry_expr_list_st())
def test_parse_object(json_document, qry_expr_list):
    instance = JmesPathParser(
        json_document=json_document,
        srch_list_expressions=qry_expr_list
    )
    result = instance.parse()
    assert len(result) <= len(instance.srch_list_expressions)
