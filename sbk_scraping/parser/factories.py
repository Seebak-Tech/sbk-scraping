from sbk_scraping.parser.common import HttpResponseParser
from sbk_scraping.utils import get_logger
from sbk_scraping.config import ParserConfig
import sbk_scraping.constants as cnst
from attrs import define


logger = get_logger(__name__)


@define()
class ParserFactory():

    config: ParserConfig

    @classmethod
    def build_from_config(cls, config_dict: dict):
        return cls(ParserConfig(config_dict))

    def __build_null_parser(self, config_dict: dict):
        msg = '\n*Cause: The json file has invalid parser_type'\
            '\n*Action: The valid values for parser_type are'\
            ' (HtmlXml, Json)'
        raise ValueError(msg)

    def __build_scrapy_parser(self,
                              config_dict: dict) -> HttpResponseParser:
        from sbk_scraping.parser.scrapy_parser import HtmlXmlParser
        parser_id = config_dict[cnst.CONFIG_PARSER_ID_KEY]
        logger.info(f'Building a HtmlXml parser({parser_id})')
        return HtmlXmlParser(
            srch_list_expressions=config_dict[cnst.CONFIG_SRCH_LST_EXPR_KEY]
        )

    def __build_json_parser(self,
                            config_dict: dict) -> HttpResponseParser:
        from sbk_scraping.parser.dynamic.json_parser import JsonParser
        parser_id = config_dict[cnst.CONFIG_PARSER_ID_KEY]
        logger.info(f'Building a Json parser({parser_id})')
        return JsonParser(
            srch_list_expressions=config_dict[cnst.CONFIG_SRCH_LST_EXPR_KEY]
        )

    def build_parser(self, parser_id: str) -> HttpResponseParser:

        parser_dict = self.get_parser_config(parser_id)
        parser_type = parser_dict[cnst.CONFIG_PARSER_TYPE_KEY]

        switcher = {
            "HtmlXml": self.__build_scrapy_parser,
            "Json": self.__build_json_parser
        }
        return switcher.get(
            parser_type,
            self.__build_null_parser
        )(parser_dict)

    def get_parser_config(self, parser_id: str) -> dict:
        return self.config.get_parser_config(parser_id)

    def set_srchex(self, parser_id: str, target_id: str, srchex: str) -> None:
        return self.config.set_srchex(parser_id, target_id, srchex)

    def get_srchex(self, parser_id: str, target_id: str) -> str:
        return self.config.get_srchex(parser_id, target_id)

    def add_srch_expression(self, parser_id: str,
                            srch_expr_dict: dict) -> None:
        self.config.add_srch_expression(parser_id, srch_expr_dict)
