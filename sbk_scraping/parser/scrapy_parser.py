import sbk_scraping.parser.common as cmn
import sbk_scraping.constants as cnst
from pydantic import conlist
from typing import Any, Pattern
import abc
from sbk_scraping.utils import get_logger


logger = get_logger(__name__)


class HtmlXmlParser(abc.ABC):

    @abc.abstractmethod
    def parse(self, data: str) -> Any:
        pass


class HtmlXmlParserFactory(cmn.HttpResponseParser, HtmlXmlParser):

    def __init__(self, srch_list_expressions: list, **kargs):
        self.srch_list_expressions = srch_list_expressions
        self.kargs = kargs

    def parse(self, data):
        if self.kargs.get(cnst.ATTR_REGEX):
            return RegexSelectorParser(
                srch_list_expressions=self.srch_list_expressions,
                **self.kargs
            ).parse(data=data)
        else:
            return HtmlXmlSelectorParser(
                srch_list_expressions=self.srch_list_expressions
            ).parse(
                data=data
            )


class HtmlXmlSelectorParser(cmn.BaseModel, HtmlXmlParser):
    srch_list_expressions: conlist(cmn.SrchTypeExpression, min_items=1)

    def parse(self, data: str) -> dict:
        from scrapy.selector import Selector
        result = {}
        field_value = []
        parser = Selector(text=data)

        for expression in self.srch_list_expressions:
            if expression.expr_type == cnst.XPATH_TYPE:
                field_value = parser.xpath(expression.srchex).getall()
            elif expression.expr_type == cnst.CSS_TYPE:
                field_value = parser.css(expression.srchex).getall()
            if field_value in [None, '', []]:
                continue
            result[expression.target_id] = field_value

        return result


class RegexSelectorParser(cmn.BaseModel, HtmlXmlParser):
    srch_list_expressions: conlist(cmn.SrchTypeExpression, min_items=1)
    regex: Pattern

    def parse(self, data: str) -> dict:
        from scrapy.selector import Selector
        result = {}
        field_value = []
        parser = Selector(text=data)

        for expression in self.srch_list_expressions:
            if expression.expr_type == cnst.XPATH_TYPE:
                field_value = parser.xpath(expression.srchex).re(self.regex)
            elif expression.expr_type == cnst.CSS_TYPE:
                field_value = parser.css(expression.srchex).re(self.regex)
            if field_value in [None, '', []]:
                continue
            result[expression.target_id] = field_value

        return result
