import jmespath
from typing import Any
from sbk_scraping.utils import load_parsers
from sbk_scraping.parser.common import HttpResponseParser, NullParser
from dataclasses import dataclass


class InvalidValue(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


@dataclass
class ParserFactory():
    data: Any
    parser_id: str

    def __build_scrapy_parser(self, expressions):
        from sbk_scraping.parser.scrapy_parser import HtmlXmlParser
        return HtmlXmlParser(
            data_body=self.data,
            srch_list_expressions=expressions
        )

    def __build_json_parser(self, expressions):
        from sbk_scraping.parser.dynamic.json_parser import JsonParser
        return JsonParser(
            data_body=self.data,
            srch_list_expressions=expressions
        )

    def __get_config_parser(self) -> dict:
        jmes_expr = f"parsers[?parser_id=='{self.parser_id}'] | [0]"
        conf_parser = jmespath.search(
            expression=jmes_expr, data=load_parsers()
        )
        if conf_parser is None:
            msg = '\n*Cause: The json file has invalid parser_id'\
                  '\n*Action: Validate the parse id'
            raise InvalidValue(msg)
        return conf_parser

    def __parser_json(self, conf_parser):
        return self.__build_json_parser(conf_parser['srch_expressions'])

    def __parser_htmlxml(self, conf_parser):
        return self.__build_scrapy_parser(conf_parser['srch_expressions'])

    def __build_parser(self, conf_parser) -> HttpResponseParser:
        parser = NullParser()
        parser_type = conf_parser["parser_type"]

        if parser_type == "HtmlXml":
            parser = self.__parser_htmlxml(conf_parser)
        elif parser_type == "Json":
            parser = self.__parser_json(conf_parser)
        else:
            msg = '\n*Cause: The json file has invalid parser_type'\
                  '\n*Action: The valid values for parser_type are'\
                  ' (HtmlXml, Json)'
            raise InvalidValue(msg)
        return parser

    def build(self) -> HttpResponseParser:
        conf_parser = self.__get_config_parser()
        return self.__build_parser(conf_parser)
