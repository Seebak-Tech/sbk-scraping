# Project
PROJECT_NAME = 'sbk-scraping'
PROJECT_PREFIX = 'SBK'

# Relative PATHs to the working directory
CONFIG_PATH = 'config'

# Test
TEST_DATA_PATH = 'tests/test_data'

# Configuration constants
CONFIG_PARSERS_KEY = 'parsers'
CONFIG_SRCH_EXPR_KEY = 'srchex'
CONFIG_SRCH_LST_EXPR_KEY = 'srch_expressions'
CONFIG_PARSER_ID_KEY = 'parser_id'
CONFIG_TARGET_ID_KEY = 'target_id'
CONFIG_PARSER_TYPE_KEY = 'parser_type'

CONFIG_KEYS = [CONFIG_PARSERS_KEY, CONFIG_SRCH_EXPR_KEY,
               CONFIG_SRCH_LST_EXPR_KEY, CONFIG_PARSER_ID_KEY,
               CONFIG_TARGET_ID_KEY, CONFIG_PARSER_TYPE_KEY]
# LISTS
INVALID_INDEX_LST = -1

# CONFIG FILES
LOGGER_FILE_NAME = 'logging_config.yaml'
PARSER_FILE_NAME = 'parsers.yaml'

# Environment Constants
ENVIRONMENT_DEV = 'DEV'
ENVIRONMENT_PROD = 'PROD'
ENVIRONMENT_TEST = 'TEST'

# Defaults
DEFAULT_WORKSPACE = '/workspace'

# Parser types
XPATH_TYPE = 'xpath'
CSS_TYPE = 'css'

# Regex for HtmlXmlParser
ATTR_REGEX = 'regex'
