import jmespath
import sbk_scraping.parser.common as cmn
from pydantic import BaseModel, conlist, validator


class JmesPathParser(BaseModel, cmn.HttpResponseParser):
    json_document: dict
    srch_list_expressions: conlist(cmn.SearchExpression, min_items=1)

    @validator('json_document')
    def _has_elements_json_document(cls, field_value):
        has_items = bool(field_value)
        if has_items:
            return field_value
        else:
            raise cmn.InvalidValue(
                "\n*Cause: The json_document field should contain at least "
                "one element to be parsed"
                "\n*Action: Please pass an a valid json dictionary"
            )

    @validator('srch_list_expressions', pre=True)
    def _check_min_num_elements(cls, field_value):
        if len(field_value) != 0:
            return field_value
        else:
            raise cmn.InvalidValue(
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
                result.append((qry_expression.target_field, qry_result))

        return result
