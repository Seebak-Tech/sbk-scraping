import environ
import enum
import attr
import sbk_scraping.constants as cnst
from pathlib import Path


def ensure_path_exists(instance, atribute, path):
    msg = f'\n*Cause: The {atribute.name} contains an invalid Path'\
          f'\n*Action: Ensure that ({path}) be a valid Path'
    if not path.exists():
        raise ValueError(msg)


class Env(enum.Enum):
    PROD = cnst.ENVIRONMENT_PROD
    DEV = cnst.ENVIRONMENT_DEV
    TEST = cnst.ENVIRONMENT_TEST


@environ.config(prefix=cnst.PROJECT_PREFIX)
class AppConfig:

    workspace = environ.var(
        default=cnst.DEFAULT_WORKSPACE,
        converter=Path,
        validator=ensure_path_exists
    )

    projectname = environ.var(default=cnst.PROJECT_NAME)

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
            lambda self: self.rootdir/cnst.TEST_DATA_PATH,
            takes_self=True
        ),
        validator=ensure_path_exists
    )

    env = environ.var(default=cnst.ENVIRONMENT_TEST, converter=Env)
