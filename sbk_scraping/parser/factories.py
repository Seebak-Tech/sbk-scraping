from sbk_scraping.parser.common import HttpResponseParser
from sbk_scraping.utils import get_logger
import sbk_scraping.constants as cnst
from attrs import define, field


logger = get_logger(__name__)


@define()
class ParserConfig:
    parsers_config: dict = field(default={})

    @parsers_config.validator
    def validate_config(self, attribute, value) -> None:
        from sbk_utils.data.validators import validate_dict_keys, instance_of

        instance_of(
            value,
            attr_type=attribute.type
        )
        #  self.__is_instance_of(value, attribute.type)

        validate_dict_keys(
            srch_dict=value,
            valid_keys=cnst.CONFIG_KEYS
        )

    def __is_instance_of(self, value, attribute_type):
        if not isinstance(value, attribute_type):
            attr_type = attribute_type.__name__
            msg = "\n*Cause: The parsers configuration should be"\
                  f" an a {attr_type} object"\
                  "\nAction: Pass the the appropiate type"
            raise ValueError(msg)

    def __raise_invalid_parse_id(self, parser_id: str) -> None:
        msg = f"\n*Cause: The parser_id: ['{parser_id}'] wasn't found"\
              "\n*Action: Validate that the parser_id is correct"
        raise ValueError(msg)

    def __raise_invalid_target_id(self, target_id: str) -> None:
        msg = f"\n*Cause: The target_id: ['{target_id}'] wasn't found"\
              "\n*Action: Validate that the target_id is correct"
        raise ValueError(msg)

    def __find_parser_idx(self, parser_id: str) -> int:
        parser_idx = cnst.INVALID_INDEX_LST
        for idx, parser in enumerate(self
                                     .parsers_config
                                     [cnst.CONFIG_PARSERS_KEY]):
            if parser[cnst.CONFIG_PARSER_ID_KEY] == parser_id:
                parser_idx = idx
                break

        if parser_idx == cnst.INVALID_INDEX_LST:
            self.__raise_invalid_parse_id(parser_id)

        return parser_idx

    def __find_srch_expr_idx(self, parser_idx: int, target_id: str) -> int:
        srch_expr_idx = cnst.INVALID_INDEX_LST
        for idx, srch_expr in enumerate(
            self
            .parsers_config
            [cnst.CONFIG_PARSERS_KEY]
            [parser_idx]
            [cnst.CONFIG_SRCH_LST_EXPR_KEY]
        ):
            if srch_expr[cnst.CONFIG_TARGET_ID_KEY] == target_id:
                srch_expr_idx = idx
                break

        if srch_expr_idx == cnst.INVALID_INDEX_LST:
            self.__raise_invalid_target_id(target_id)

        return srch_expr_idx

    def get_parser_config(self, parser_id: str) -> dict:
        import jmespath

        jmes_expr = f"parsers[?parser_id=='{parser_id}'] | [0]"
        conf_parser = jmespath.search(
            expression=jmes_expr,
            data=self.parsers_config
        )
        if conf_parser is None:
            self.__raise_invalid_parse_id(parser_id)
        return conf_parser

    def set_srchex(self, parser_id: str, target_id: str, srchex: str) -> None:

        parser_idx = self.__find_parser_idx(parser_id)
        srch_expr_idx = self.__find_srch_expr_idx(parser_idx, target_id)
        (self.parsers_config[cnst.CONFIG_PARSERS_KEY]
                            [parser_idx]
                            [cnst.CONFIG_SRCH_LST_EXPR_KEY]
                            [srch_expr_idx]
                            [cnst.CONFIG_SRCH_EXPR_KEY]) = srchex

    def get_srchex(self, parser_id: str, target_id: str) -> str:
        import jmespath

        expr_by_parser_id = f"parsers[?parser_id=='{parser_id}']|[0]"
        expr_by_target_id = f"srch_expressions[?target_id=='{target_id}']|[0]"\
                            ".srchex"

        srchex = expr_by_parser_id + '.' + expr_by_target_id
        result = jmespath.search(
            expression=srchex,
            data=self.parsers_config
        )
        if result is None:
            msg = f"\n*Cause: The object with the parser_id: ['{parser_id}']"\
                  " or target_id: ['{target_id}'] wasn't found"\
                  "\n*Action: Validate that both ids are correct"
            raise ValueError(msg)

        return result

    def add_srch_expression(self, parser_id: str,
                            srch_expr_dict: dict) -> None:
        parser_idx = self.__find_parser_idx(parser_id)

        (self
         .parsers_config
         [cnst.CONFIG_PARSERS_KEY]
         [parser_idx]
         [cnst.CONFIG_SRCH_LST_EXPR_KEY]
         .append(srch_expr_dict))


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
        from sbk_scraping.parser.scrapy_parser import HtmlXmlParserFactory
        parser_id = config_dict[cnst.CONFIG_PARSER_ID_KEY]
        logger.info(f'Building a HtmlXml parser({parser_id})')
        return HtmlXmlParserFactory(
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
