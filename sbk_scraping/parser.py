import warnings
import jmespath
from typing import Optional
from pydantic import BaseModel, conlist, constr, validator, root_validator

warnings.filterwarnings("ignore", category=DeprecationWarning)

class InvalidValue(Exception):
    def __init__(self, message: str) -> None:
        # Genereates error message
        super().__init__(message)


class HttpResponseParser():
    def parse(self):
        pass


class JmesPathExpression(BaseModel):
    expr_tag: constr(strip_whitespace=True, regex=r'\w+')
    srch_expression: constr(strip_whitespace=True, min_length=2)
    expr_description: Optional[str] = None

    @root_validator(pre=True)
    def _check_ommited_srch_expression(cls, field_values):
        field_name = 'SRCH_EXPRESSION'
        has_mandatory_fields = (
            bool(field_values.get('expr_tag')) and
            bool(field_values.get('srch_expression'))
        )
        if bool(field_values.get('expr_tag')):
            field_name = 'EXPR_TAG'
        if has_mandatory_fields:
            return field_values
        else:
            raise InvalidValue(
                f"\n*Cause: The field {field_name} should contain a value"
                "\n*Action: Please input some valid strings to the field"
            )


class JmesPathParser(BaseModel, HttpResponseParser):
    json_document: dict
    srch_list_expressions: conlist(JmesPathExpression, min_items=1)

    @validator('json_document')
    def _has_elements_json_document(cls, field_value):
        has_items = bool(field_value)
        if has_items:
            return field_value
        else:
            raise InvalidValue(
                "\n*Cause: The json_document field should contain at least "
                "one element to be parsed"
                "\n*Action: Please pass an a valid json dictionary"
            )

    @validator('srch_list_expressions', pre=True)
    def _check_min_num_elements(cls, field_value):
        if len(field_value) != 0:
            return field_value
        else:
            raise InvalidValue(
                "\n*Cause: At least one search expression should exist to be "
                "able to extract elements from the json document"
                "\n*Action: Please pass at least one search expression"
            )

    def parse(self) -> list:
        result = []
        for qry_expression in self.srch_list_expressions:
            qry_result = jmespath.search(
                expression=qry_expression.srch_expression,
                data=self.json_document
            )
            if bool(qry_result):
                result.append((qry_expression.expr_tag, qry_result))

        return result
