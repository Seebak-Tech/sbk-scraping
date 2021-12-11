import abc
from pydantic import BaseModel, constr, root_validator
from typing import Optional, Any


class HttpResponseParser(abc.ABC):
    @abc.abstractmethod
    def parse(self) -> Any:
        pass


class InvalidValue(Exception):
    def __init__(self, message: str) -> None:
        # Genereates error message
        super().__init__(message)


class SearchExpression(BaseModel):
    target_field: constr(strip_whitespace=True, regex=r'\w+')
    expr_type: constr(strip_whitespace=True, regex=r'\w+')
    srch_expression: constr(strip_whitespace=True, min_length=1)
    expr_description: Optional[str] = None

    @root_validator(pre=True)
    def _check_ommited_srch_expression(cls, field_values):
        field_name = 'SRCH_EXPRESSION'
        has_mandatory_fields = (
            bool(field_values.get('target_field')) and
            bool(field_values.get('srch_expression'))
        )
        if bool(field_values.get('target_field')):
            field_name = 'EXPR_TAG'
        if has_mandatory_fields:
            return field_values
        else:
            raise InvalidValue(
                f"\n*Cause: The field {field_name} should contain a value"
                "\n*Action: Please input some valid strings to the field"
            )
