import sbk_scraping.parser.common as cmn
from pydantic import conlist, constr


class InvalidSrchExprType(Exception):
    def __init__(self, mensaje):
        Exception.__init__(self, mensaje)


class HtmlXmlParser(cmn.BaseModel, cmn.HttpResponseParser):
    data_body: constr(min_length=1)
    srch_list_expressions: conlist(cmn.SrchTypeExpression, min_items=1)

    def parse(self) -> dict:
        from scrapy.selector import Selector
        result = {}
        field_value = []
        parser = Selector(text=self.data_body)

        for expression in self.srch_list_expressions:
            if expression.expr_type == 'xpath':
                field_value = parser.xpath(expression.srch_expression).getall()
            elif expression.expr_type == 'css':
                field_value = parser.css(expression.srch_expression).getall()
            else:
                msg = f'\n*Cause: The expression type is invalid'\
                    f'\n*Action: Validate the following expression'\
                    f' type exists: ({expression.expr_type})'
                raise InvalidSrchExprType(msg)
            if field_value in [None, '', []]:
                continue
            result[expression.target_field] = field_value

        return result
