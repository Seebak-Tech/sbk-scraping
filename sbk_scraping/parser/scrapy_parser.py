import sbk_scraping.parser.common as cmn
from pydantic import conlist, constr
from typing import Optional


class HtmlXmlParser(cmn.BaseModel, cmn.HttpResponseParser):
    data_body: constr(min_length=1)
    srch_list_expressions: conlist(cmn.SearchExpression, min_items=1)
    srch_list_expr_type: Optional[cmn.SearchExpressionType]

    def parse(self) -> dict:
        from scrapy.selector import Selector
        result = {}
        field_value = []
        parser = Selector(text=self.data_body)
        srch_list_expressions = self.srch_list_expressions

        for expr_type in self.srch_list_expr_type:
            if expr_type.expr_type == 'xpath':
                field_value = parser.xpath(
                    srch_list_expressions.srch_expression
                ).getall()
            elif expr_type.expr_type == 'css':
                field_value = parser.css(
                    srch_list_expressions.srch_expression
                ).getall()
            if field_value in [None, '', []]:
                continue
            result[srch_list_expressions.target_field] = field_value

        return result
