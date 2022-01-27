import sbk_scraping.parser.common as cmn
import sbk_scraping.constants as cnst
from pydantic import conlist, constr


class HtmlXmlParser(cmn.BaseModel, cmn.HttpResponseParser):
    data_body: constr(min_length=1)
    srch_list_expressions: conlist(cmn.SrchTypeExpression, min_items=1)

    def parse(self) -> dict:
        from scrapy.selector import Selector
        result = {}
        field_value = []
        parser = Selector(text=self.data_body)

        for expression in self.srch_list_expressions:
            if expression.expr_type == cnst.XPATH_TYPE:
                field_value = parser.xpath(expression.srchex).getall()
            elif expression.expr_type == cnst.CSS_TYPE:
                field_value = parser.css(expression.srchex).getall()
            if field_value in [None, '', []]:
                continue
            result[expression.target_id] = field_value

        return result
