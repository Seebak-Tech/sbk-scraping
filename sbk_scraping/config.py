import environ
import enum
import attr
from pathlib import Path
from attrs import define, field, validators
from sbk_scraping.parser.common import InvalidValue


def ensure_path_exists(instance, atribute, path):
    msg = f'\n*Cause: The {atribute.name} contains an invalid Path'\
          f'\n*Action: Ensure that ({path}) be a valid Path'
    if not path.exists():
        raise ValueError(msg)


class Env(enum.Enum):
    PROD = "production"
    DEV = "development"
    TEST = "test"


@environ.config(prefix='SBK')
class AppConfig:

    workspace = environ.var(
        default='/workspace',
        converter=Path,
        validator=ensure_path_exists
    )

    projectname = environ.var(default='sbk-scraping')

    rootdir = environ.var(
        default=attr.Factory(
            lambda self: self.workspace/self.projectname,
            takes_self=True
        ),
        converter=Path,
        validator=ensure_path_exists
    )

    testdata = environ.var(
        default=attr.Factory(
            lambda self: self.rootdir/'tests'/'test_data',
            takes_self=True
        ),
        validator=ensure_path_exists
    )

    env = environ.var(default="test", converter=Env)


@define()
class ParserConfig:
    parsers_config: dict = field(default={})

    @parsers_config.validator
    def _validate_params(self, attribute, value) -> None:
        self.__is_instance_of(value, attribute.type)
        self.__fit_dictionary_keys(value)

    def __is_instance_of(self, value, attribute_type):
        if not isinstance(value, attribute_type):
            attr_type = attribute_type.__name__
            msg = "\n*Cause: The parsers configuration should be"\
                  f" an a {attr_type} object"\
                  "\nAction: Pass the the appropiate type"
            raise InvalidValue(msg)

    def __fit_dictionary_keys(self, value):
        if "parsers" not in value:
            msg = "\n*Cause: The keys: ['parsers'] should exists "\
                  "in the configuration"\
                  "\n*Action: Add the appropiate keys to the config dictionary"
            raise InvalidValue(msg)

    def __raise_invalid_parse_id(self, parser_id: str) -> None:
        msg = f"\n*Cause: The parser_id: ['{parser_id}'] wasn't found"\
              "\n*Action: Validate that the parser_id is correct"
        raise InvalidValue(msg)

    def __raise_invalid_target_id(self, target_id: str) -> None:
        msg = f"\n*Cause: The target_id: ['{target_id}'] wasn't found"\
              "\n*Action: Validate that the target_id is correct"
        raise InvalidValue(msg)

    def __find_parser_idx(self, parser_id: str) -> int:
        parser_idx = -1
        for idx, parser in enumerate(self.parsers_config['parsers']):
            if parser['parser_id'] == parser_id:
                parser_idx = idx
                break

        if parser_idx == -1:
            self.__raise_invalid_parse_id(parser_id)

        return parser_idx

    def __find_srch_expr_idx(self, parser_idx: int, target_id: str) -> int:
        srch_expr_idx = -1
        for idx, srch_expr in enumerate(
            self.parsers_config['parsers'][parser_idx]['srch_expressions']
        ):
            if srch_expr['target_id'] == target_id:
                srch_expr_idx = idx
                break

        if srch_expr_idx == -1:
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
        (self.parsers_config['parsers']
                            [parser_idx]
                            ['srch_expressions']
                            [srch_expr_idx]
                            ['srchex']) = srchex

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
            raise InvalidValue(msg)

        return result

    def add_srch_expression(self, parser_id: str, **kwargs) -> None:
        parser_idx = self.__find_parser_idx(parser_id)
        (self.parsers_config['parsers']
                            [parser_idx]
                            ['srch_expressions'].append(kwargs))
