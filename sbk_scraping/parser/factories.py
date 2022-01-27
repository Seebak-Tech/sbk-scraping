from typing import Union
from dataclasses import dataclass
from sbk_scraping.parser.common import HttpResponseParser, InvalidValue
from sbk_scraping.utils import get_logger
from sbk_scraping.config import ParserConfig


logger = get_logger(__name__)


@dataclass
class ParserFactory():

    config: ParserConfig

    @classmethod
    def build_from_config(cls, config_dict: dict):
        return cls(ParserConfig(config_dict))

    def __build_null_parser(self, config_dict: dict,
                            data: Union[str, dict]):
        msg = '\n*Cause: The json file has invalid parser_type'\
            '\n*Action: The valid values for parser_type are'\
            ' (HtmlXml, Json)'
        raise InvalidValue(msg)

    def __build_scrapy_parser(self,
                              config_dict: dict,
                              data: str) -> HttpResponseParser:
        from sbk_scraping.parser.scrapy_parser import HtmlXmlParser
        parser_id = config_dict["parser_id"]
        logger.info(f'Building a HtmlXml parser({parser_id})')
        return HtmlXmlParser(
            data_body=data,
            srch_list_expressions=config_dict['srch_expressions']
        )

    def __build_json_parser(self,
                            config_dict: dict,
                            data: dict) -> HttpResponseParser:
        from sbk_scraping.parser.dynamic.json_parser import JsonParser
        parser_id = config_dict["parser_id"]
        logger.info(f'Building a Json parser({parser_id})')
        return JsonParser(
            json_document=data,
            srch_list_expressions=config_dict['srch_expressions']
        )

    def build_parser(self,
                     data: Union[dict, str],
                     parser_id: str) -> HttpResponseParser:

        parser_dict = self.config.get_parser_config(parser_id)
        parser_type = parser_dict["parser_type"]

        switcher = {
            "HtmlXml": self.__build_scrapy_parser,
            "Json": self.__build_json_parser
        }
        return switcher.get(
            parser_type,
            self.__build_null_parser
        )(parser_dict, data)
