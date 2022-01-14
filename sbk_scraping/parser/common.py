import abc
from pydantic import BaseModel as PydanticBaseModel, constr
from typing import Optional, Any, Literal


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
        msg6 = '*Cause: This field should contain at least {limit_value} '\
               'characters\n'\
               '  *Action: Ensure this field has the minimum number '\
               'of characters'
        msg7 = '*Cause: This field should be a string type\n'\
               '  *Action: Provide a valid value'
        msg8 = '*Cause: The field value is not a valid dict\n'\
               '  *Action: Provide an a dictionary object'
        msg9 = '*Cause: The field value ({given}) is invalid\n'\
               '  *Action: The permitted values are:'\
               '  ({permitted}), considere this is case sensitive'

        error_msg_templates = {
            'value_error.missing': msg1,
            'value_error.str.regex': msg2,
            'value_error.list.min_items': msg3,
            'type_error.none.not_allowed': msg4,
            'type_error.list': msg5,
            'value_error.any_str.min_length': msg6,
            'type_error.str': msg7,
            'type_error.dict': msg8,
            'value_error.const': msg9
        }


class HttpResponseParser(abc.ABC):
    @abc.abstractmethod
    def parse(self) -> Any:
        pass


class NullParser(HttpResponseParser):
    def parse(self):
        pass


class SearchExpression(BaseModel):
    target_field: constr(strip_whitespace=True, regex=r'\w+')
    srch_expression: constr(strip_whitespace=True, min_length=1)
    expr_description: Optional[str] = None


class SrchTypeExpression(SearchExpression):
    expr_type: Literal['xpath', 'css']
