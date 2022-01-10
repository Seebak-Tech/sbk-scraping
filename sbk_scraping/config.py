import environ
import enum
import attr
from pathlib import Path


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
