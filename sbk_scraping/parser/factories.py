import jmespath
from typing import Union
from dataclasses import dataclass
from sbk_scraping.parser.common import HttpResponseParser, NullParser
from sbk_scraping.utils import get_logger, load_config_file


logger = get_logger(__name__)


class InvalidValue(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


@dataclass
class ParserFactory():
    data: Union[dict, str]
    parser_id: str

    def __build_scrapy_parser(self, conf_parser):
        from sbk_scraping.parser.scrapy_parser import HtmlXmlParser
        logger.info('Building a HtmlXml parser')
        return HtmlXmlParser(
            data_body=self.data,
            srch_list_expressions=conf_parser['srch_expressions']
        )

    def __build_json_parser(self, conf_parser):
        from sbk_scraping.parser.dynamic.json_parser import JsonParser
        logger.info('Building a Json parser')
        return JsonParser(
            json_document=self.data,
            srch_list_expressions=conf_parser['srch_expressions']
        )

    def __get_config_parser(self) -> dict:
        jmes_expr = f"parsers[?parser_id=='{self.parser_id}'] | [0]"
        conf_parser = jmespath.search(
            expression=jmes_expr, data=load_config_file('parsers.json')
        )
        if conf_parser is None:
            msg = '\n*Cause: The json file has invalid parser_id'\
                  '\n*Action: Validate the parse id'
            raise InvalidValue(msg)
        return conf_parser

    def __build_parser(self, conf_parser) -> HttpResponseParser:
        parser = NullParser()
        parser_type = conf_parser["parser_type"]

        if parser_type == "HtmlXml":
            parser = self.__build_scrapy_parser(conf_parser)
        elif parser_type == "Json":
            parser = self.__build_json_parser(conf_parser)
        else:
            msg = '\n*Cause: The json file has invalid parser_type'\
                  '\n*Action: The valid values for parser_type are'\
                  ' (HtmlXml, Json)'
            raise InvalidValue(msg)
        return parser

    def build(self) -> HttpResponseParser:
        return self.__build_parser(self.__get_config_parser())
