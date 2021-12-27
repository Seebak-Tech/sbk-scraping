import abc
from pydantic import BaseModel as PydanticBaseModel, constr
from typing import Optional, Any


class BaseModel(PydanticBaseModel):
    class Config:
        msg1 = '*Cause: This field is mandatory\n'\
               '  *Action: Provide a valid value for this field'
        msg2 = '*Cause: The field value does not match the regex\n'\
               '  *Action: Input a valid value that satisfy the regex pattern'
        msg3 = '*Cause: The list should have at least {limit_value} items\n'\
               '  *Action: Provide a list with the minimum number of items'
        msg4 = '*Cause: None is not an allowed value\n'\
               '  *Action: Provide a valid value'
        msg5 = '*Cause: This field is not a valid list\n'\
               '  *Action: Provide an a list object'
        error_msg_templates = {
            'value_error.missing': msg1,
            'value_error.str.regex': msg2,
            'value_error.list.min_items': msg3,
            'type_error.none.not_allowed': msg4,
            'type_error.list': msg5,
        }


class HttpResponseParser(abc.ABC):
    @abc.abstractmethod
    def parse(self) -> Any:
        pass


class InvalidValue(Exception):
    def __init__(self, message: str) -> None:
        # Genereates error message
        super().__init__(message)


class InvalidType(Exception):
    def __init__(self, message: str) -> None:
        # Genereates error message
        super().__init__(message)


class SearchExpression(BaseModel):
    target_field: constr(strip_whitespace=True, regex=r'\w+')
    expr_type: constr(strip_whitespace=True, regex=r'\w+')
    srch_expression: constr(strip_whitespace=True, min_length=1)
    expr_description: Optional[str] = None
