import jmespath
from typing import Any
from sbk_scraping.utils import load_parsers
from sbk_scraping.parser.common import HttpResponseParser, NullParser
from dataclasses import dataclass


class InvalidParserType(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class InvalidParseId(Exception):
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
        cfg_parser = jmespath.search(
            expression=jmes_expr, data=load_parsers()
        )
        if cfg_parser is None:
            msg = '\n*Cause: The json file has invalid parser id'\
                  '\n*Action: Validate the parse id'
            raise InvalidParseId(msg)
        return cfg_parser

    def __parser_json(self, cfg_parser):
        parser = self.__build_json_parser(cfg_parser['srch_expressions'])
        return parser

    def __parser_htmlxml(self, cfg_parser):
        parser = self.__build_scrapy_parser(cfg_parser['srch_expressions'])
        return parser

    def __build_parser(self) -> HttpResponseParser:
        parser = NullParser()
        cfg_parser = self.__get_config_parser()
        parser_type = cfg_parser["parser_type"]

        msg = '\n*Cause: The json file has invalid parser type'\
              '\n*Action: Please validate the parser type'
        
        if parser_type == "HtmlXml":
            self.__parser_htmlxml(cfg_parser)
        elif parser_type == "Json":
            self.__parser_json(cfg_parser)
        else:
            raise InvalidParserType(msg)
        return parser

    def build(self) -> HttpResponseParser:
        return self.__build_parser()

    #  def __build_parser(self) -> HttpResponseParser:
        #  parser = NullParser()
        #  cfg_parser = self.__get_config_parser()
#
        #  msg = '\n*Cause: The json file has invalid parser type'\
              #  '\n*Action: Please validate the parser type'
#
        #  if cfg_parser["parser_type"] == "HtmlXml":
            #  parser = self.__build_scrapy_parser(cfg_parser['srch_expressions'])
        #  elif cfg_parser["parser_type"] == "Json":
            #  parser = self.__build_json_parser(cfg_parser['srch_expressions'])
        #  else:
            #  raise InvalidParserType(msg)
        #  return parser

