import jmespath
import environ
from sbk_scraping.config import AppConfig
from sbk_scraping.utils import load_json_file, read_parsers
import sbk_scraping.parser.common as cmn


class ParserFactory(cmn.BaseModel):
    config: AppConfig

    def parser_type(self, config):
        json_file = read_parsers(config)
        qry_result = jmespath.search(
            expression='parsers[*].parser_type)',
            data=json_file
        )
        print(qry_result)
        if qry_result == 'HtmlXml':
            pass
        elif qry_result == 'Json':
            pass


# validar tipo de parser
# Validar para ese parser, que los srch_expressions types sean los correctos
# -para el HtmlXml los tipos deben ser css y xpath
# - para Json , deben ser type json
