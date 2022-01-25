import environ
import enum
import attr
from pathlib import Path
from dataclasses import dataclass, field


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


class InvalidValue(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


@dataclass()
class ParserConfig:
    parsers_config: dict = field(default_factory=dict)

    def __find_parser_idx(self, parser_id: str) -> int:
        parser_idx = None

        for idx, parser in enumerate(self.parsers_config['parsers']):
            if parser['parser_id'] == parser_id:
                parser_idx = idx
                break

        if parser_idx is None:
            msg = '\n*Cause: The configuration for Parser:{parser_id} '\
                  'was not found'\
                  '\n*Action: Validate that the parser id is correct'

            raise InvalidValue(msg)

        return parser_idx

    def __find_srch_expr_idx(self, parser_idx: int, target_id: str) -> int:
        srch_expr_idx = None

        for idx, srch_expr in enumerate(
            self.parsers_config['parsers'][parser_idx]['srch_expressions']
        ):
            if srch_expr['target_id'] == target_id:
                srch_expr_idx = idx
                break

        if srch_expr_idx is None:
            msg = '\n*Cause: The srchex was not set because the '\
                  f'target_id:{target_id} were not found'\
                  '\n*Action: Validate that the target_id of the '\
                  'search_expressions is correct'

            raise InvalidValue(msg)

        return srch_expr_idx

    def get_parser_config(self, parser_id: str) -> dict:
        import jmespath

        jmes_expr = f"parsers[?parser_id=='{parser_id}'] | [0]"
        conf_parser = jmespath.search(
            expression=jmes_expr,
            data=self.parsers_config
        )
        if conf_parser is None:
            msg = '\n*Cause: The object has an invalid parser_id'\
                  '\n*Action: Validate that the parser_id is correct'
            raise InvalidValue(msg)
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
            msg = '\n*Cause: The object was not found with '\
                  f'the parser_id:{parser_id} and target_id:{target_id}'\
                  '\n*Action: Validate that both ids are correct'
            raise InvalidValue(msg)

        return result

    #  def add_srch_expression(self, parser_id: str, **kwargs) -> None:
    #      pass
